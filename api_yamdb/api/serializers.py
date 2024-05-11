# serializers.py
from rest_framework import serializers
from users.models import CustomUser
from django.core.validators import RegexValidator
from rest_framework.validators import UniqueValidator


class UserWithoutTokenSerializer(serializers.ModelSerializer):
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
    email = serializers.EmailField(
        required=True,
        max_length=254,
        validators=[
            UniqueValidator(
                queryset=CustomUser.objects.all(),
                message="Пользователь с этим email уже зарегистрирован."
            )
        ])

    class Meta:
        model = CustomUser
        fields = ['username', 'email']


class UserTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True,
                                     max_length=150)
    confirmation_code = serializers.CharField(required=True,
                                              max_length=6)

    class Meta:
        model = CustomUser
        fields = ['username', 'confirmation_code']


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
