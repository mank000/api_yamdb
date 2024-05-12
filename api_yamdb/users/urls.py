from .views import (signup, get_token, update_profile)
from django.urls import path, include
from rest_framework.routers import SimpleRouter
router = SimpleRouter()

router.register('users', update_profile)


urlpatterns = [
    path('api/v1/auth/signup/', signup, name='signup'),
    path('api/v1/auth/token/', get_token, name='get_token'),
    path('api/v1/', include(router.urls)),
]
