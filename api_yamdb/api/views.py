from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment
from api.serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    GenreTitleSerializer,
    ReviewSerializer,
    CommentSerializer,
)


class CategoryViewSet(viewsets.ModelViewSet):
    """Представление для работы с моделью категория."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(viewsets.ModelViewSet):
    """Представление для работы с моделью жанр."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для работы с моделью титл."""

    queryset = Title.objects.all()
    serializer_class = TitleSerializer


class GenreTitleViewSet(viewsets.ModelViewSet):
    """Представление для работы с моделью микс титл и жанр."""

    queryset = GenreTitle.objects.all()
    serializer_class = GenreTitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для работы с моделью отзыв."""

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для работы с моделью коммент."""

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_review(self):
        """Получаем отзыв для комментария."""
        return get_object_or_404(
            Review,
            id=self.kwargs.get("review_id"),
            title__id=self.kwargs.get("title_id"),
        )

    def get_queryset(self):
        """Получаем queryset."""
        return self.get_review().comments_review.all()

    def perform_create(self, serializer):
        """Переопределяем метод create."""
        serializer.save(review=self.get_review(), author=self.request.user)
