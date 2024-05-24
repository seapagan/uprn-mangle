"""Define schemas used in this applicaition."""

from pydantic import BaseModel


class AddressCreate(BaseModel):
    """Pydantic model used for creating the address table."""

    UPRN: int
    SUB_BUILDING_NAME: str = ""
    BUILDING_NAME: str = ""
    BUILDING_NUMBER: str = ""
    THOROUGHFARE: str = ""
    POST_TOWN: str = ""
    POSTCODE: str = ""
    ADMINISTRATIVE_AREA: str = ""
    LOGICAL_STATUS: str = ""
    BLPU_STATE: str = ""
    X_COORDINATE: float = 0.0
    Y_COORDINATE: float = 0.0
    LATITUDE: float = 0.0
    LONGITUDE: float = 0.0
    COUNTRY: str = ""
    CLASSIFICATION_CODE: str = ""
    USRN: str = ""
    STREET_DESCRIPTION: str = ""
    LOCALITY: str = ""
    TOWN_NAME: str = ""


class UPRNResponse(BaseModel):
    """Pydantic model used for returning UPRN data."""

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
