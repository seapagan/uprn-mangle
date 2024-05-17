"""Pydantic and SQLAlchemy models for the address table."""

from pydantic import BaseModel
from sqlalchemy import BigInteger, Column, Float, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Address(Base):
    """SQLAlchemy model for the address table."""

    __tablename__ = "addressbase"
    UPRN = Column(BigInteger, primary_key=True, index=True)
    FULL_ADDRESS = Column(String, nullable=False)
    SUB_BUILDING_NAME = Column(String)
    BUILDING_NAME = Column(String)
    BUILDING_NUMBER = Column(String)
    THOROUGHFARE = Column(String)
    POST_TOWN = Column(String)
    POSTCODE = Column(String)
    ADMINISTRATIVE_AREA = Column(String)
    LOGICAL_STATUS = Column(String)
    BLPU_STATE = Column(String)
    X_COORDINATE = Column(Float)
    Y_COORDINATE = Column(Float)
    LATITUDE = Column(Float)
    LONGITUDE = Column(Float)
    COUNTRY = Column(String)
    CLASSIFICATION_CODE = Column(String)
    USRN = Column(String)
    STREET_DESCRIPTION = Column(String)
    LOCALITY = Column(String)
    TOWN_NAME = Column(String)


class AddressCreate(BaseModel):
    """Pydantic model for the address table."""

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
