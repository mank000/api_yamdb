from rest_framework import serializers
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title
from users.models import CustomUser



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
        fields = ("name", "slug")
        
   

class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Жанра."""
    class Meta:
        model = Genre
        fields = ("name", "slug")


class TitleSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Произведения."""
    class Meta:
        model = Title
        fields = ("id", "name", "year", "description", "genre", "category")


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
        fields = ("id", "text", "author", "score", "title", "pub_date")

class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Комментария."""
    author = serializers.SlugRelatedField("author",
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ("id", "text", "author", "review", "pub_date")
