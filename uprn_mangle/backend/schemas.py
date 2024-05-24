"""Define schemas used in this applicaition."""

from pydantic import BaseModel, ConfigDict


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

    model_config = ConfigDict(from_attributes=True)

    UPRN: int
    FULL_ADDRESS: str
    POSTCODE: str
    X_COORDINATE: float
    Y_COORDINATE: float
    LATITUDE: float
    LONGITUDE: float
    COUNTRY: str
    CLASSIFICATION_CODE: str
    STREET_DESCRIPTION: str
