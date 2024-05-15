from django.forms import ValidationError
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import YamdbUser


class UserWithoutTokenSerializer(serializers.ModelSerializer):
    """Сериализатор формы регистрации."""

    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = YamdbUser
        fields = ('username', 'email')

    def validate_username(self, username):
        if username.lower() == 'me':
            raise ValidationError({"message": "недопустимый username"})
        return username

    def validate(self, data):
        if YamdbUser.objects.filter(username=data['username']).exists():
            user = YamdbUser.objects.get(username=data['username'])
            if user.email == data['email']:
                return data
            raise ValidationError({"message": "Неверный email"})
        return data


class UserTokenSerializer(serializers.ModelSerializer):
    """Сериализатор получения JWT-токена."""

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = YamdbUser
        fields = ('username', 'confirmation_code')

    def validate_username(self, username):
        if YamdbUser.objects.filter(username=username).exists():
            return username
        raise Http404('Недопустимое имя пользователя или пользователь'
                      f'`{username}` не найден.')

    def validate(self, data):
        # Получаем пользователя по имени пользователя (username)
        user = YamdbUser.objects.filter(username=data.get('username')).first()
        if not user:
            raise ValidationError({"Ошибка": 'Пользователь не найден'})
        return data


class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор кастомной модели User."""

    username = serializers.SlugField(
        max_length=150,
        validators=[UniqueValidator(queryset=YamdbUser.objects.all())]
    )
    email = serializers.EmailField(
        max_length=254,
        validators=[UniqueValidator(queryset=YamdbUser.objects.all())]
    )

    class Meta:
        model = YamdbUser

        fields = (
            'username', 'email', 'first_name', 'last_name', 'bio', 'role'
        )
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категории."""

    class Meta:
        model = Category
        fields = ("name", "slug")


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Жанра."""

    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleCreateSerializer(serializers.ModelSerializer):
    """Сериализатор создания произведений."""

    name = serializers.CharField(
        max_length=200,
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
    )

    class Meta:
        model = Title
        fields = (
            '__all__'
        )


class TitleReciveSerializer(serializers.ModelSerializer):
    """Сериализатор получения произведений."""

    category = CategorySerializer(
        read_only=True,
    )
    genre = GenreSerializer(
        many=True,
        read_only=True,
    )
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = '__all__'
        read_only_fields = (
            'id', 'name', 'year', 'rating', 'description',
        )


class GenreTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Соответствия жанра и произведения."""

    class Meta:
        model = GenreTitle
        fields = ("id", "genre", "title")


class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Отзыва."""

    author = serializers.StringRelatedField(
        read_only=True
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "pub_date")

    def validate(self, attrs):
        if not self.context.get('request').method == 'POST':
            return attrs
        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)

        if Review.objects.filter(author=author, title=title).exists():
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв на это произведение.'
            )

        return attrs


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Комментария."""

    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "pub_date")
