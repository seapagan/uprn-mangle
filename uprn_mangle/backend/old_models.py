"""This is the old model for the Addressbase data.

This will be re-implemented as a pydantic model for the new API.
Keeping this here for reference.
"""

# mypy: ignore-errors
from django.contrib.postgres.indexes import GinIndex
from django.contrib.postgres.search import SearchVectorField
from django.db import models


class Addressbase(models.Model):
    """Define the Addressbase model.

    This model is used to store the Addressbase data.
    """

    uprn = models.BigIntegerField(
        db_column="UPRN", blank=False, null=False, primary_key=True
    )
    full_address = models.TextField(
        db_column="FULL_ADDRESS", blank=True, default=""
    )
    sub_building_name = models.TextField(
        db_column="SUB_BUILDING_NAME", blank=True, default=""
    )
    building_name = models.TextField(
        db_column="BUILDING_NAME", blank=True, default=""
    )
    building_number = models.TextField(
        db_column="BUILDING_NUMBER", blank=True, default=""
    )
    thoroughfare = models.TextField(
        db_column="THOROUGHFARE", blank=True, default=""
    )
    post_town = models.TextField(db_column="POST_TOWN", blank=True, default="")
    postcode = models.TextField(db_column="POSTCODE", blank=True, default="")
    logical_status = models.BigIntegerField(
        db_column="LOGICAL_STATUS", blank=True, default=""
    )
    blpu_state = models.TextField(
        db_column="BLPU_STATE", blank=True, default=""
    )
    x_coordinate = models.FloatField(
        db_column="X_COORDINATE", blank=True, default=""
    )
    y_coordinate = models.FloatField(
        db_column="Y_COORDINATE", blank=True, default=""
    )
    latitude = models.FloatField(db_column="LATITUDE", blank=True, default="")
    longitude = models.FloatField(db_column="LONGITUDE", blank=True, default="")
    country = models.TextField(db_column="COUNTRY", blank=True, default="")
    classification_code = models.TextField(
        db_column="CLASSIFICATION_CODE", blank=True, default=""
    )
    usrn = models.TextField(db_column="USRN", blank=True, default="")
    street_description = models.TextField(
        db_column="STREET_DESCRIPTION", blank=True, default=""
    )
    locality = models.TextField(db_column="LOCALITY", blank=True, default="")
    town_name = models.TextField(db_column="TOWN_NAME", blank=True, default="")
    administrative_area = models.TextField(
        db_column="ADMINISTRATIVE_AREA", blank=True, default=""
    )
    tsv = SearchVectorField(null=True)

    class Meta:
        """Meta class for the Addressbase model."""

        managed = True
        db_table = "addressbase"
        indexes = (GinIndex(fields=["tsv"]),)

    def __str__(self) -> str:
        """Return the string representation of the model instance."""
        return self.full_address
