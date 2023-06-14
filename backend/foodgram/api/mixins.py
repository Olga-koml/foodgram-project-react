from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.viewsets import GenericViewSet


class GetListCreateDeleteMixin(GenericViewSet, CreateModelMixin,
                               ListModelMixin, DestroyModelMixin):
    """Вспомогательный класс для настройки вьюсета.
    Может отображать список, создавать, удалять"""
    pass
