from rest_framework import serializers
from reviews.models import Category, Comment, Genre, GenreTitle, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для модели Категории."""
    class Meta:
        model = Category
        fields = ("id", "name", "slug")
        4
        5
        66
        5
        66
        7
        7799


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели Жанра."""
    class Meta:
        model = Genre
        fields = ("id", "name", "slug")


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
