from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin,
                                   RetrieveModelMixin)
from rest_framework.viewsets import GenericViewSet


class GetListCreateDeleteMixin(GenericViewSet, CreateModelMixin,
                               ListModelMixin, DestroyModelMixin):
    pass
