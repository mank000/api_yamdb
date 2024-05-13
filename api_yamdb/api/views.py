from django.shortcuts import get_object_or_404
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions, status, viewsets
from rest_framework.pagination import LimitOffsetPagination

from .utils import send_to_email, make_confirmation_code
from rest_framework.decorators import api_view, permission_classes

from api.filters import TitleFilter
from reviews.models import Category, Genre, Title, GenreTitle, Review, Comment
from users.models import CustomUser
from api.permissions import (
    ChangeAdminOnly, StaffOrReadOnly, AuthorOrStaffOrReadOnly, CustomPermission, TestPerm
    )


from api.mixins import ModelMixinSet
from api.serializers import (
    UsersSerializer,
    CategorySerializer,
    GenreSerializer,
    TitleReciveSerializer,
    TitleCreateSerializer,
    #TitleSerializer,
    GenreTitleSerializer,
    ReviewSerializer,
    CommentSerializer,
    UserWithoutTokenSerializer
)
from users.models import CustomUser

#CustomUser = get_user_model()

@api_view(['POST'])
def signup(request):
    serializer = UserWithoutTokenSerializer(data=request.data)

    if (serializer.is_valid()):

        existing_user_username = CustomUser.objects.filter(
            username=serializer.validated_data.get('username'))
       
        existing_user_email = CustomUser.objects.filter(
            email=serializer.validated_data.get('email'))
        
        existing_user = CustomUser.objects.filter(
            username=serializer.validated_data.get('username'),
            email=serializer.validated_data.get('email'))

        if (existing_user_username and existing_user_username.first().username == serializer.validated_data.get("username")
                and existing_user_username.first().email != serializer.validated_data.get("email")):
            return Response({"message": "Пользователь уже зарегистрирован"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if (existing_user_username
                and existing_user_username.first().username == serializer.validated_data.get("username")
                and existing_user_username.first().email == serializer.validated_data.get("email")
                and existing_user_username.first().confirmation_code != ""):
            return Response({"message": "Пользователь уже зарегистрирован"},
                                        status=status.HTTP_200_OK)

        if (existing_user_email.exists()
                and not existing_user_username.exists()):
            return Response({"message": "Пользователь уже зарегистрирован"},
                            status=status.HTTP_400_BAD_REQUEST)
        
        if (existing_user_email or existing_user or existing_user_username):
            return Response({"message": "Пользователь уже зарегистрирован"},
                            status=status.HTTP_200_OK)

        user = serializer.save()
        confirmation_code = make_confirmation_code()
        user.confirmation_code = confirmation_code
        sended = send_to_email(serializer.validated_data.get("email"),
                               confirmation_code)
        user.save()

        if sended == 0:
            return Response({"error": "Ошибка отправки письма. "
                             "Свяжитесь с администратором"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)

@api_view(['PATCH', "POST", "GET"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    if request.method == "POST":
        serializer = UserCreateSerializer(data=request.data)
        if (serializer.is_valid()
                and serializer.validated_data.get("username") != "me"):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    if request.method == "GET":

        search_query = request.GET.get('search', None)
        paginator = LimitOffsetPagination()
        paginator.page_size = 10

        if search_query:
            users = CustomUser.objects.filter(username=search_query)
        else:
            users = CustomUser.objects.all()

        paginated_users = paginator.paginate_queryset(users, request=request)
        serializer = UserSearchSerializer(paginated_users, many=True)
        print(paginated_users)
        response_data = {
            'count': paginator.count,
            'results': paginated_users,
        }

        return paginator.get_paginated_response(response_data)



@api_view(['POST'])
def get_token(request):
    seralizer = UserTokenSerializer(data=request.data)
    if seralizer.is_valid():
        user = get_object_or_404(
            CustomUser,
            username=seralizer.validated_data.get("username")
        )
        if (user.confirmation_code
                == seralizer.validated_data.get("confirmation_code")):
            refresh = RefreshToken.for_user(user)
            user.confirmation_code = ''
            user.save()
            return Response({'token': str(refresh.access_token)},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неправильный код!'},
                            status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)




class UserViewSet(viewsets.ModelViewSet):
    """Работа с пользователями."""
    queryset = CustomUser.objects.all()
    serializer_class = UsersSerializer
    permission_classes = (ChangeAdminOnly,)
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


class CategoryViewSet(ModelMixinSet):
    """Представление для работы с моделью категория."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = ( permissions.IsAuthenticatedOrReadOnly,)
    #                      AnonimReadOnly,)
    #permission_classes = (CustomPermission,)
    permission_classes = (StaffOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ("name",)
    lookup_field = "slug"


class GenreViewSet(ModelMixinSet):
    """Представление для работы с моделью жанр."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (StaffOrReadOnly,)
    #permission_classes = (CustomPermission,)
    filter_backends = (SearchFilter, )
    search_fields = ("name",)
    lookup_field = "slug"


class TitleViewSet(viewsets.ModelViewSet):
    """Представление для работы с моделью титл."""
    http_method_names = ['get', 'post', 'patch', 'delete']    
    queryset = Title.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    #serializer_class = TitleSerializer
    permission_classes = (StaffOrReadOnly,)
    pagination_class = LimitOffsetPagination
    serializer_class = TitleReciveSerializer
    # filter_backends = (SearchFilter,)
    # search_fields = ['genre__slug',]

    def get_queryset(self):
        return Title.objects.annotate(rating=Avg('reviews__score'))
    


    def get_serializer_class(self):
        """
        Переопределяем метод get_serializer_class()
        для проверки какаяоперация REST
        была использована и возвращаем серриализаторы
        для записи и чтения.
        """
        if self.action in ['list', 'retrieve']:
            return TitleReciveSerializer
        return TitleCreateSerializer




# class GenreTitleViewSet(viewsets.ModelViewSet):
#     """Представление для работы с моделью произведение."""

#     queryset = GenreTitle.objects.all()
#     serializer_class = GenreTitleSerializer
#     permission_classes = (ChangeAdminOnly)


class ReviewViewSet(viewsets.ModelViewSet):
    """Представление для работы с моделью отзыв."""

    # queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = ( permissions.IsAuthenticatedOrReadOnly,
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
        """Создает отзыв для текущего произведения,
        где автором является текущий пользователь."""
        serializer.save(
            author=self.request.user,
            title=self.get_title()
        )


class CommentViewSet(viewsets.ModelViewSet):
    """Представление для работы с моделью коммент."""

    # queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
#                            TestPerm,)
                          AuthorOrStaffOrReadOnly,)
#                            CustomPermission,)
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_review(self):
        """Получаем отзыв для комментария."""
        return get_object_or_404(
            Review,
            pk=self.kwargs.get("review_id"),
            # title__id=self.kwargs.get("title_id"),
        )


    def get_queryset(self):
        """Возвращает queryset c комментариями для текущего отзыва."""
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        """Переопределяем метод create."""
        serializer.save(review=self.get_review(), author=self.request.user)
