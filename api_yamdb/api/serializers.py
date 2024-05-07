from rest_framework import serializers
from reviews.models import (
    Category, Comment,
    Genre, GenreTitle, Review, Title
)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')


class GenreTitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = GenreTitle
        fields = ('id', 'genre', 'title')


class ReviewSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(source='publishedmodel.pub_date', read_only=True)
    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'title', 'pub_date')


class CommentSerializer(serializers.ModelSerializer):
    pub_date = serializers.DateTimeField(source='publishedmodel.pub_date', read_only=True)
    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'review', 'pub_date')
        