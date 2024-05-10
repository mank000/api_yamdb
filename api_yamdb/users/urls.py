from .views import (signup, get_token, update_profile)
from django.urls import path


urlpatterns = [
    path('api/v1/auth/signup/', signup, name='signup'),
    path('api/v1/auth/token/', get_token, name='get_token'),
    path('api/v1/users/', update_profile, name='update_profile'),
    path('api/v1/users/', update_profile, name='update_profile'),
]
