from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken


from api.filters import TitleFilter
from api.mixins import ModelMixinSet
from api.permissions import (
    AuthorOrStaffOrReadOnly,
    ChangeAdminOnly,
    StaffOrReadOnly
)
from api.serializers import (
    CategorySerializer,
    CommentSerializer,
    GenreSerializer,
    ReviewSerializer,
    TitleCreateSerializer,
    TitleReciveSerializer,
    UsersSerializer,
    UserTokenSerializer,
    UserWithoutTokenSerializer,
)
from api.utils import (
    make_confirmation_code,
    send_to_email
)
from reviews.models import Category, Genre, Review, Title
from users.models import YamdbUser


class SignView(APIView):

    def post(self, request):
        serializer = UserWithoutTokenSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")

        existing_user = YamdbUser.objects.filter(
            username=username,
            email=email
        )

        if existing_user.exists():
            user = existing_user.first()
        else:
            user = serializer.save()

        confirmation_code = make_confirmation_code()
        user.confirmation_code = confirmation_code
        sended = send_to_email(
            serializer.validated_data.get("email"),
            confirmation_code
        )
        user.save()

        if sended == 0:
            return Response({"error": "Ошибка отправки письма. "
                            "Свяжитесь с администратором"},
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.data,
                        status=status.HTTP_200_OK)


class GetTokenView(APIView):
    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = get_object_or_404(
            YamdbUser,
            username=serializer.validated_data.get("username")
        )
        refresh = RefreshToken.for_user(user)
        user.confirmation_code = ''
        user.save()
        return Response({'token': str(refresh.access_token)},
                        status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    """Работа с пользователями."""

    queryset = YamdbUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (ChangeAdminOnly,)
    search_fields = ("username",)
    filter_backends = (SearchFilter,)
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
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(ModelMixinSet):
    """Представление для работы с моделью категория."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(ModelMixinSet):
    """Представление для работы с моделью жанр."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для работы с моделью титл."""

    filter_backends = (DjangoFilterBackend, OrderingFilter)
    ordering_fields = ('name', 'year', 'category__slug', 'rating')
    filterset_class = TitleFilter
    permission_classes = (StaffOrReadOnly,)
    pagination_class = LimitOffsetPagination
    serializer_class = TitleReciveSerializer
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        return Title.objects.annotate(
            rating=Avg('reviews__score')).order_by('-rating')

    def get_serializer_class(self):
        """Переопределяем метод для чтения и создания."""
        if self.action in ['list', 'retrieve']:
            return TitleReciveSerializer
        return TitleCreateSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для работы с моделью отзыв."""

    serializer_class = ReviewSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          AuthorOrStaffOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_title(self):
        """Возвращает объект текущего произведения."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        """Возвращает queryset c отзывами для текущего произведения."""
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        """Создает авторский отзыв."""
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для работы с моделью коммент."""

    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          AuthorOrStaffOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        """Возвращает отзыв для комментария."""
        return get_object_or_404(
            Review,
            pk=self.kwargs.get("review_id"),
        )

    def get_queryset(self):
        """Возвращает queryset c комментариями для текущего отзыва."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Переопределяет метод create."""
        serializer.save(review=self.get_review(), author=self.request.user)
