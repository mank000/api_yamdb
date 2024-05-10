from django.core.exceptions import ValidationError
from django.http import Http404
from rest_framework import serializers
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import CustomUser


class SignUpSerializer(serializers.ModelSerializer):
    """
    Сериализатор формы регистрации.
    """

    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = CustomUser
        fields = ('username', 'email')

    def validate_username(self, username):
        if username.lower() == 'me':
            raise ValidationError({"message": "недопустимый username"})
        return username

    def validate(self, data):
        if CustomUser.objects.filter(username=data['username']).exists():
            user = CustomUser.objects.get(username=data['username'])
            if user.email == data['email']:
                return data
            raise ValidationError({"message": "Неверный email"})
        return data


class ActivationSerializer(serializers.ModelSerializer):
    """
    Сериализатор получения JWT-токена.
    """

    username = serializers.CharField(max_length=150)
    confirmation_code = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('username', 'confirmation_code')

    def validate_username(self, username):
        if CustomUser.objects.filter(username=username).exists():
            return username
        raise Http404(f'Недопустимое имя пользователя или пользователь `{username}` не найден.')

    def validate(self, data):
        # Получаем пользователя по имени пользователя (username)
        user = CustomUser.objects.filter(username=data.get('username')).first()
        if not user:
            raise ValidationError({"Ошибка": 'Пользователь не найден'})  # Изменяем сообщение об ошибке
        # if data.get('confirmation_code') != user.confirmation_code:
        #     raise ValidationError({"Ошибка": 'Неверный код подтверждения'})
        # return data

    

class UsersSerializer(serializers.ModelSerializer):
    """Сериализатор кастомной модели User."""
    username = serializers.SlugField(max_length=150)
    email = serializers.EmailField(max_length=254)

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )
        read_only_fields = ('username', 'email', 'role',)


class AdminSerializer(serializers.ModelSerializer):
    """Сериализатор администратора с доступом к ролям."""
    role = serializers.ChoiceField(
        choices=CustomUser.ROLE_CHOICES, required=False
        )

    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'first_name',
            'last_name', 'bio', 'role',
        )


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категории."""
    class Meta:
        model = Category
        fields = ("id", "name", "slug")
   

class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Жанра."""
    class Meta:
        model = Genre
        fields = ("id", "name", "slug")


# class TitleSerializer(serializers.ModelSerializer):
#     genre = serializers.SlugRelatedField(
#         slug_field='slug', queryset=Genre.objects.all(), many=True
#     )

#     class Meta:
#         model = Title
#         fields = ('id', 'name', 'year', 'description', 'genre', 'category')


# class GenreTitleSerializer(serializers.ModelSerializer):
#     category = CategorySerializer(
#         read_only=True,
#     )
#     genre = GenreSerializer(
#         many=True,
#         read_only=True,
#     )
#     title = serializers.SlugRelatedField(
#         slug_field='name', queryset=Title.objects.all()
#     )
#     rating = serializers.FloatField()

#     class Meta:
#         model = GenreTitle
#         fields = ['genre', 'title']

#предыдущее
# class GenreSerializer(serializers.ModelSerializer):
#     """Сериализатор для модели Жанра."""
#     class Meta:
#         model = Genre
#         fields = ("id", "name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Произведения."""
    rating = serializers.FloatField()

    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")


# class TitleCreateSerializer(serializers.ModelSerializer):
#     """
#     Сериализатор создания произведений.
#     """

#     name = serializers.CharField(
#         max_length=200,
#     )
#     category = serializers.SlugRelatedField(
#         queryset=Category.objects.all(),
#         slug_field='slug',
#     )
#     genre = serializers.SlugRelatedField(
#         queryset=Genre.objects.all(),
#         slug_field='slug',
#         many=True,
#     )

#     class Meta:
#         model = Title
#         fields = (
#             '__all__'
#         )


# class TitleReciveSerializer(serializers.ModelSerializer):
#     """
#     Сериализатор получения произведений.
#     """

#     category = CategorySerializer(
#         read_only=True,
#     )
#     genre = GenreSerializer(
#         many=True,
#         read_only=True,
#     )
#     rating = serializers.FloatField()

#     class Meta:
#         model = Title
#         fields = '__all__'
#         read_only_fields = (
#             'id', 'name', 'year', 'rating', 'description',
#         )



class GenreTitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Соответствия жанра и произведения."""
    class Meta:
        model = GenreTitle
        fields = ("id", "genre", "title")



class ReviewSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Отзыва."""
    pub_date = serializers.DateTimeField(
        source="publishedmodel.pub_date", read_only=True
    )

    class Meta:
        model = Review
        fields = ("id", "text", "author", "score", "title", "pub_date")


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Комментария."""
    pub_date = serializers.DateTimeField(
        source="publishedmodel.pub_date", read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "review", "pub_date")
