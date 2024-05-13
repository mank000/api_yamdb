# from rest_framework import status
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response
# from api.serializers import (UserWithoutTokenSerializer,
#                              UserTokenSerializer,
#                              UsersSerializer)
# from .utils import send_to_email, make_confirmation_code
# from .models import CustomUser
# from django.shortcuts import get_object_or_404
# from rest_framework_simplejwt.tokens import RefreshToken
# from rest_framework.pagination import LimitOffsetPagination
# from rest_framework.decorators import action
# from rest_framework import viewsets
# from api.permissions import (
#     ChangeAdminOnly, StaffOrReadOnly, AuthorOrStaffOrReadOnly
# )
# from rest_framework import permissions

# @api_view(['POST'])
# def signup(request):
#     serializer = UserWithoutTokenSerializer(data=request.data)

#     if (serializer.is_valid()):

#         existing_user_username = CustomUser.objects.filter(
#             username=serializer.validated_data.get('username'))
       
#         existing_user_email = CustomUser.objects.filter(
#             email=serializer.validated_data.get('email'))
        
#         existing_user = CustomUser.objects.filter(
#             username=serializer.validated_data.get('username'),
#             email=serializer.validated_data.get('email'))

#         if (existing_user_username and existing_user_username.first().username == serializer.validated_data.get("username")
#                 and existing_user_username.first().email != serializer.validated_data.get("email")):
#             return Response({"message": "Пользователь уже зарегистрирован"},
#                             status=status.HTTP_400_BAD_REQUEST)
        
#         if (existing_user_username
#                 and existing_user_username.first().username == serializer.validated_data.get("username")
#                 and existing_user_username.first().email == serializer.validated_data.get("email")
#                 and existing_user_username.first().confirmation_code != ""):
#             return Response({"message": "Пользователь уже зарегистрирован"},
#                                         status=status.HTTP_200_OK)

#         if (existing_user_email.exists()
#                 and not existing_user_username.exists()):
#             return Response({"message": "Пользователь уже зарегистрирован"},
#                             status=status.HTTP_400_BAD_REQUEST)
        
#         if (existing_user_email or existing_user or existing_user_username):
#             return Response({"message": "Пользователь уже зарегистрирован"},
#                             status=status.HTTP_200_OK)

#         user = serializer.save()
#         confirmation_code = make_confirmation_code()
#         user.confirmation_code = confirmation_code
#         sended = send_to_email(serializer.validated_data.get("email"),
#                                confirmation_code)
#         user.save()

#         if sended == 0:
#             return Response({"error": "Ошибка отправки письма. "
#                              "Свяжитесь с администратором"},
#                             status=status.HTTP_400_BAD_REQUEST)

#         return Response(serializer.data,
#                         status=status.HTTP_200_OK)
#     return Response(serializer.errors,
#                     status=status.HTTP_400_BAD_REQUEST)


# # class update_profile(viewsets.ModelViewSet):
# #     """Работа с пользователями."""
# #     queryset = CustomUser.objects.all()
# #     serializer_class = UsersSerializer
# #     permission_classes = (ChangeAdminOnly,)
# #     search_fields = ("username",)
# #     lookup_field = "username"
# #     http_method_names = ['get', 'post', 'patch', 'delete']

# #     @action(
# #         detail=False, methods=['get', 'patch'],
# #         url_path='me', url_name='me',
# #         permission_classes=(permissions.IsAuthenticated,)
# #     )
# #     def my_profile(self, request):
# #         serializer = UsersSerializer(request.user)
# #         if request.method == 'PATCH':
# #             serializer = UsersSerializer(
# #                 request.user, data=request.data, partial=True
# #             )
# #             serializer.is_valid(raise_exception=True)
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_200_OK)
# #         return Response(serializer.data, status=status.HTTP_200_OK)

# # def get_paginated_response(NumberPagination):
# #     def get_paginated_response(self, data):
# #         return Response(
# #             {
# #                 'count': NumberPagination.count,
# #                 'next': NumberPagination.get_next_link(),
# #                 'previous': NumberPagination.get_previous_link(),
# #                 'results': data
# #             }
# #         )


# # @api_view(['PATCH', "POST", "GET"])
# # @permission_classes([IsAuthenticated])
# # def update_profile(request):
# #     if request.method == "POST":
# #         serializer = UserCreateSerializer(data=request.data)
# #         if (serializer.is_valid()
# #                 and serializer.validated_data.get("username") != "me"):
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# #     if request.method == "GET":

# #         search_query = request.GET.get('search', None)
# #         paginator = LimitOffsetPagination()
# #         paginator.page_size = 10

# #         if search_query:
# #             users = CustomUser.objects.filter(username=search_query)
# #         else:
# #             users = CustomUser.objects.all()

# #         paginated_users = paginator.paginate_queryset(users, request=request)
# #         serializer = UserSearchSerializer(paginated_users, many=True)
# #         print(paginated_users)
# #         response_data = {
# #             'count': paginator.count,
# #             'results': paginated_users,
# #         }

# #         return paginator.get_paginated_response(response_data)



# @api_view(['POST'])
# def get_token(request):
#     seralizer = UserTokenSerializer(data=request.data)
#     if seralizer.is_valid():
#         user = get_object_or_404(
#             CustomUser,
#             username=seralizer.validated_data.get("username")
#         )
#         if (user.confirmation_code
#                 == seralizer.validated_data.get("confirmation_code")):
#             refresh = RefreshToken.for_user(user)
#             user.confirmation_code = ''
#             user.save()
#             return Response({'token': str(refresh.access_token)},
#                             status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Неправильный код!'},
#                             status=status.HTTP_400_BAD_REQUEST)

#     else:
#         return Response(seralizer.errors, status=status.HTTP_400_BAD_REQUEST)
