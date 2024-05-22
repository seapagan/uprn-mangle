"""Pydantic and SQLAlchemy models for the address table."""

from pydantic import BaseModel
from sqlalchemy import BigInteger, Column, Float, Index, MetaData, String
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for SQLAlchemy models."""

    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )


class Address(Base):
    """SQLAlchemy model for the address table."""

    __tablename__ = "addressbase"

    UPRN: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    FULL_ADDRESS: Mapped[str] = mapped_column(String(255), nullable=False)
    SUB_BUILDING_NAME: Mapped[str] = mapped_column(String(64))
    BUILDING_NAME: Mapped[str] = mapped_column(String(64))
    BUILDING_NUMBER: Mapped[str] = mapped_column(String(8))
    THOROUGHFARE: Mapped[str] = mapped_column(String(64))
    POST_TOWN: Mapped[str] = mapped_column(String(64))
    POSTCODE: Mapped[str] = mapped_column(String(10))
    ADMINISTRATIVE_AREA: Mapped[str] = mapped_column(String(64))
    LOGICAL_STATUS: Mapped[str] = mapped_column(String(64))
    BLPU_STATE: Mapped[str] = mapped_column(String(64))
    X_COORDINATE: Mapped[float] = mapped_column(Float)
    Y_COORDINATE: Mapped[float] = mapped_column(Float)
    LATITUDE: Mapped[float] = mapped_column(Float)
    LONGITUDE: Mapped[float] = mapped_column(Float)
    COUNTRY: Mapped[str] = mapped_column(String(64))
    CLASSIFICATION_CODE: Mapped[str] = mapped_column(String(64))
    USRN: Mapped[str] = mapped_column(String(20))
    STREET_DESCRIPTION: Mapped[str] = mapped_column(String(255))
    LOCALITY: Mapped[str] = mapped_column(String(64))
    TOWN_NAME: Mapped[str] = mapped_column(String(64))
    TSV = Column(TSVECTOR)

    __table_args__ = (
        Index(
            "ix_addressbase_tsv", "TSV", postgresql_using="gin"
        ),  # Index for improving search performance
    )


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
