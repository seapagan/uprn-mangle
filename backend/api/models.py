from django.db import models


class Addressbase(models.Model):
    uprn = models.BigIntegerField(
        db_column="UPRN", blank=False, null=False
    )  # Field name made lowercase.
    full_address = models.TextField(
        db_column="FULL_ADDRESS", blank=True, null=True
    )  # Field name made lowercase.
    sub_building_name = models.TextField(
        db_column="SUB_BUILDING_NAME", blank=True, null=True
    )  # Field name made lowercase.
    building_name = models.TextField(
        db_column="BUILDING_NAME", blank=True, null=True
    )  # Field name made lowercase.
    building_number = models.TextField(
        db_column="BUILDING_NUMBER", blank=True, null=True
    )  # Field name made lowercase.
    thoroughfare = models.TextField(
        db_column="THOROUGHFARE", blank=True, null=True
    )  # Field name made lowercase.
    post_town = models.TextField(
        db_column="POST_TOWN", blank=True, null=True
    )  # Field name made lowercase.
    postcode = models.TextField(
        db_column="POSTCODE", blank=True, null=True
    )  # Field name made lowercase.
    logical_status = models.BigIntegerField(
        db_column="LOGICAL_STATUS", blank=True, null=True
    )  # Field name made lowercase.
    blpu_state = models.TextField(
        db_column="BLPU_STATE", blank=True, null=True
    )  # Field name made lowercase.
    x_coordinate = models.FloatField(
        db_column="X_COORDINATE", blank=True, null=True
    )  # Field name made lowercase.
    y_coordinate = models.FloatField(
        db_column="Y_COORDINATE", blank=True, null=True
    )  # Field name made lowercase.
    latitude = models.FloatField(
        db_column="LATITUDE", blank=True, null=True
    )  # Field name made lowercase.
    longitude = models.FloatField(
        db_column="LONGITUDE", blank=True, null=True
    )  # Field name made lowercase.
    country = models.TextField(
        db_column="COUNTRY", blank=True, null=True
    )  # Field name made lowercase.
    classification_code = models.TextField(
        db_column="CLASSIFICATION_CODE", blank=True, null=True
    )  # Field name made lowercase.
    usrn = models.TextField(
        db_column="USRN", blank=True, null=True
    )  # Field name made lowercase.
    street_description = models.TextField(
        db_column="STREET_DESCRIPTION", blank=True, null=True
    )  # Field name made lowercase.
    locality = models.TextField(
        db_column="LOCALITY", blank=True, null=True
    )  # Field name made lowercase.
    town_name = models.TextField(
        db_column="TOWN_NAME", blank=True, null=True
    )  # Field name made lowercase.
    administrative_area = models.TextField(
        db_column="ADMINISTRATIVE_AREA", blank=True, null=True
    )  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = "addressbase"
