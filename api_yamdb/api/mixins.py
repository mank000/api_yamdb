from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin
)
from rest_framework.viewsets import GenericViewSet
from rest_framework.filters import SearchFilter

from api.permissions import (StaffOrReadOnly)


class ModelMixinSet(
    CreateModelMixin, ListModelMixin,
    DestroyModelMixin, GenericViewSet
):
    permission_classes = (StaffOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ("name",)
    lookup_field = "slug"
