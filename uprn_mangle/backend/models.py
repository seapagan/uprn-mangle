"""Pydantic and SQLAlchemy models for the address table."""

from sqlalchemy import BigInteger, Column, Float, Index, String
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column

from uprn_mangle.backend.database import Base


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

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"Address({self.UPRN} @ {self.FULL_ADDRESS})"
