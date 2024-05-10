# views.py
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from api.serializers import UserWithoutTokenSerializer, UserTokenSerializer
from .utils import send_to_email, make_confirmation_code
from .models import CustomUser
from django.shortcuts import get_object_or_404
from rest_framework_simplejwt.tokens import RefreshToken


@api_view(['POST'])
def signup(request):
    serializer = UserWithoutTokenSerializer(data=request.data)
    if (serializer.is_valid()
            and serializer.validated_data.get("username") != "me"):
        user = serializer.save()
        confirmation_code = make_confirmation_code()
        user.confirmation_code = confirmation_code
        user.save()
        sended = send_to_email(serializer.validated_data.get("email"),
                               confirmation_code)
        if sended == 0:
            return Response({"error": "Ошибка отправки письма. "
                             "Свяжитесь с администратором"},
                            status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.data,
                        status=status.HTTP_200_OK)
    return Response(serializer.errors,
                    status=status.HTTP_400_BAD_REQUEST)


@api_view(['PATCH', "POST"])
@permission_classes([IsAuthenticated])
def update_profile(request):
    serializer = UserWithoutTokenSerializer(request.user,
                                            data=request.data,
                                            partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
            return Response({'token': str(refresh.access_token)},
                            status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Неправильный код!'},
                            status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
