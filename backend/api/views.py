from rest_framework import viewsets

from .models import Addressbase
from .serializers import AddressbaseSerializer


class SearchViewSet(viewsets.ModelViewSet):
    # queryset = Addressbase.objects.all().order_by("uprn")[:10]
    serializer_class = AddressbaseSerializer

    def get_queryset(self):
        # This search is very fast, using the Postgresql Full-Text-Search and
        # pre-computed ts_vectors from the 'tsv' column. These were manually
        # added. We need to add this to the import scripts. This will not be
        # needed to be implemented forreal-time since the database is static.

        srch_param = self.request.query_params.get("q")

        queryset = Addressbase.objects.all().order_by("uprn")[:20]

        if srch_param:
            # queryset = Addressbase.objects.filter(
            #     full_address__search=srch_param
            # ).order_by("uprn")
            queryset = Addressbase.objects.filter(tsv=srch_param).order_by(
                "uprn"
            )

        return queryset
