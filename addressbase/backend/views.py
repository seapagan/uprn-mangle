# from django.shortcuts import render

from rest_framework import viewsets
from rest_framework import permissions

from .serializers import AddressBaseSerializer
from .models import Addressbase


class AddressBaseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Addressbase.objects.all().order_by("uprn")
    serializer_class = AddressBaseSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
