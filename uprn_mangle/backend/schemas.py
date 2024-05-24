"""Define schemas used in this applicaition."""

from pydantic import BaseModel, ConfigDict


class AddressCreate(BaseModel):
    """Pydantic model used for creating the address table."""

    uprn: int
    sub_building_name: str = ""
    building_name: str = ""
    building_number: str = ""
    thoroughfare: str = ""
    post_town: str = ""
    postcode: str = ""
    administrative_area: str = ""
    logical_status: str = ""
    blpu_state: str = ""
    x_coordinate: float = 0.0
    y_coordinate: float = 0.0
    latitude: float = 0.0
    longitude: float = 0.0
    country: str = ""
    classification_code: str = ""
    usrn: str = ""
    street_description: str = ""
    locality: str = ""
    town_name: str = ""


class UPRNResponse(BaseModel):
    """Pydantic model used for returning UPRN data."""

    model_config = ConfigDict(from_attributes=True)

    uprn: int
    full_address: str
    postcode: str
    x_coordinate: float
    y_coordinate: float
    latitude: float
    longitude: float
    country: str
    classification_code: str
    street_description: str
