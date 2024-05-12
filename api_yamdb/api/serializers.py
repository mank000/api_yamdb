# serializers.py
from rest_framework import serializers
from users.models import CustomUser
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator, UniqueTogetherValidator
from django.core.exceptions import ValidationError
from django.http import Http404


class UserWithoutTokenSerializer(serializers.ModelSerializer):
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


class UserTokenSerializer(serializers.ModelSerializer):
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
        if data.get('confirmation_code') != user.confirmation_code:
            raise ValidationError({"Ошибка": 'Неверный код подтверждения'})
        return data


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


# class UserWithoutTokenSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(
#         required=True,
#         max_length=150,
#         validators=[
#             RegexValidator(
#                 r'^[\w.@+-]+$',
#                 'Это поле может содержать только '
#                 'буквы, цифры и @, ., +, -, _ знаки'
#             ),
#         ],
#     )
#     email = serializers.EmailField(
#         required=True,
#         max_length=254,
#     )

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'email']


# class UserTokenSerializer(serializers.ModelSerializer):
#     username = serializers.CharField(required=True,
#                                      max_length=150)
#     confirmation_code = serializers.CharField(required=True,
#                                               max_length=6)

#     class Meta:
#         model = CustomUser
#         fields = ['username', 'confirmation_code']


class UserCreateSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        required=True,
        max_length=150,
        validators=[
            RegexValidator(
                r'^[\w.@+-]+$',
                'Это поле может содержать только '
                'буквы, цифры и @, ., +, -, _ знаки'
            ),
        ],
    )
    email = serializers.EmailField(required=True,
                                   max_length=254)
    first_name = serializers.CharField(required=False, max_length=150)
    last_name = serializers.CharField(required=False, max_length=150)
    bio = serializers.CharField(required=False)
    role = serializers.CharField(required=False,
                                 default="user")

    class Meta:
        model = CustomUser
        fields = ['username',
                  'email',
                  'first_name',
                  'last_name',
                  'bio',
                  'role']


class UserSearchSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=False,
                                     max_length=150)
    
    class Meta:
        model = CustomUser
        fields = ['id', 'username',]