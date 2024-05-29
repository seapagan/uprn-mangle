"""Pydantic and SQLAlchemy models for the address table."""

from sqlalchemy import BigInteger, Column, Float, Index, String
from sqlalchemy.dialects.postgresql import TSVECTOR
from sqlalchemy.orm import Mapped, mapped_column

from uprn_mangle.backend.database import Base


class Address(Base):
    """SQLAlchemy model for the address table."""

    __tablename__ = "addressbase"

    uprn: Mapped[int] = mapped_column(BigInteger, primary_key=True, index=True)
    full_address: Mapped[str] = mapped_column(String(255), nullable=False)
    sub_building_name: Mapped[str] = mapped_column(String(64))
    building_name: Mapped[str] = mapped_column(String(64))
    building_number: Mapped[str] = mapped_column(String(8))
    thoroughfare: Mapped[str] = mapped_column(String(64))
    post_town: Mapped[str] = mapped_column(String(64))
    postcode: Mapped[str] = mapped_column(String(10))
    administrative_area: Mapped[str] = mapped_column(String(64))
    x_coordinate: Mapped[float] = mapped_column(Float)
    y_coordinate: Mapped[float] = mapped_column(Float)
    latitude: Mapped[float] = mapped_column(Float)
    longitude: Mapped[float] = mapped_column(Float)
    country: Mapped[str] = mapped_column(String(64))
    usrn: Mapped[str] = mapped_column(String(20))
    street_description: Mapped[str] = mapped_column(String(255))
    locality: Mapped[str] = mapped_column(String(64))
    town_name: Mapped[str] = mapped_column(String(64))
    tsv = Column(TSVECTOR)

    __table_args__ = (
        Index(
            "ix_addressbase_tsv", "tsv", postgresql_using="gin"
        ),  # Index for improving search performance
    )

    def __repr__(self) -> str:
        """Return a string representation of the model."""
        return f"Address({self.uprn} @ {self.full_address})"
