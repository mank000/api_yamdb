from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework import permissions, status, viewsets
from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment
from users.models import CustomUser
from api.serializers import (
    UsersSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleSerializer,
    GenreTitleSerializer,
    ReviewSerializer,
    CommentSerializer,
)


CustomUser = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    """Работа с пользователями."""
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    search_fields = ("username",)
    lookup_field = "username"
    http_method_names = ['get', 'post', 'patch', 'delete']

    @action(
        detail=False, methods=['get', 'patch'],
        url_path='me', url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def my_profile(self, request):
        serializer = UsersSerializer(request.user)
        if request.method == 'PATCH':
            serializer = UsersSerializer(
                request.user, data=request.data, partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


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
    """Представление для работы с моделью произведение."""

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
