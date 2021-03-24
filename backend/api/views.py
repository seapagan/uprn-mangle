from rest_framework import viewsets

from .models import Addressbase
from .serializers import AddressbaseSerializer


class SearchViewSet(viewsets.ModelViewSet):
    # queryset = Addressbase.objects.all().order_by("uprn")[:10]
    serializer_class = AddressbaseSerializer

    def get_queryset(self):
        srch_param = self.request.query_params.get("q")

        queryset = Addressbase.objects.all().order_by("uprn")[:20]

        if srch_param:
            queryset = Addressbase.objects.filter(
                full_address__search=srch_param
            ).order_by("uprn")

        return queryset
