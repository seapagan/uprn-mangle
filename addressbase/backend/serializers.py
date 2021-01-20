from rest_framework import serializers
from .models import Addressbase


class AddressBaseSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Addressbase
        fields = [
            "url",
            "uprn",
            "full_address",
            "x_coordinate",
            "y_coordinate",
            "latitude",
            "longitude",
            "post_town",
            "postcode",
            "locality",
            "administrative_area",
            "country",
            "logical_status",
            "blpu_state",
        ]
