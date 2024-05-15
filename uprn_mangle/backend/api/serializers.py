from rest_framework import serializers

from .models import Addressbase


class AddressbaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Addressbase
        fields = [
            "uprn",
            "full_address",
            "x_coordinate",
            "y_coordinate",
            "latitude",
            "longitude",
            "country",
            "classification_code",
            "street_description",
        ]
