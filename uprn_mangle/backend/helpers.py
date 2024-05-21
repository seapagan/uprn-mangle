"""Helper functions used by the main Class."""

import re
from pathlib import Path
from typing import Any

import dask.dataframe as dd
import pandas as pd
from dask.diagnostics.progress import ProgressBar
from rich import print as rprint
from sqlalchemy import Engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from uprn_mangle.backend.models import Address, AddressCreate, Base


def extract_record_type(filename: str) -> int:
    """Return just the record type from the filename.

    Used with the header files.
    """
    match = re.search(r"Record_(\d+)_", filename)
    if match:
        return int(match.group(1))

    msg = f"Filename {filename} does not match the expected format"
    raise ValueError(msg)


def show_header(text_list: list[str], width: int = 80) -> None:
    """Show a section Header with an arbitrary number of lines.

    Args:
        text_list (list): A list of Strings to be shown, one per line
        width (int, optional): Width to make the box. Defaults to 50.
    """
    divider = "-" * (width - 2)
    rprint("\n[green]/" + divider + "\\")
    for line in text_list:
        rprint("[green]|" + line.center((width - 2), " ") + "|")
    rprint("[green]\\" + divider + "/")


def to_parquet_with_progress(
    ddf: dd.DataFrame, filename: Path, **kwargs: dict[str, Any]
) -> None:
    """Convert a dask dataframe to parquet with a progress bar."""
    with ProgressBar():
        ddf.to_parquet(filename, **kwargs)


def generate_full_address(address: AddressCreate) -> str:
    """Generate full address by concatenating specific fields."""
    fields = [
        address.SUB_BUILDING_NAME.strip(),
        address.BUILDING_NAME.strip(),
        address.BUILDING_NUMBER.strip(),
        address.THOROUGHFARE.strip(),
        address.POST_TOWN.strip(),
        address.POSTCODE.strip(),
        address.ADMINISTRATIVE_AREA.strip(),
    ]
    return ", ".join([field for field in fields if field])


def create_address(session: Session, address: AddressCreate) -> Address | None:
    """Create a new address entry in the database."""
    if address.POSTCODE.strip() == "":
        return None  # we don't want to store addresses without a postcode

    db_address = Address(
        UPRN=address.UPRN,
        FULL_ADDRESS=generate_full_address(address),
        SUB_BUILDING_NAME=address.SUB_BUILDING_NAME,
        BUILDING_NAME=address.BUILDING_NAME,
        BUILDING_NUMBER=address.BUILDING_NUMBER,
        THOROUGHFARE=address.THOROUGHFARE,
        POST_TOWN=address.POST_TOWN,
        POSTCODE=address.POSTCODE,
        ADMINISTRATIVE_AREA=address.ADMINISTRATIVE_AREA,
        LOGICAL_STATUS=address.LOGICAL_STATUS,
        BLPU_STATE=address.BLPU_STATE,
        X_COORDINATE=address.X_COORDINATE,
        Y_COORDINATE=address.Y_COORDINATE,
        LATITUDE=address.LATITUDE,
        LONGITUDE=address.LONGITUDE,
        COUNTRY=address.COUNTRY,
        CLASSIFICATION_CODE=address.CLASSIFICATION_CODE,
        USRN=address.USRN,
        STREET_DESCRIPTION=address.STREET_DESCRIPTION,
        LOCALITY=address.LOCALITY,
        TOWN_NAME=address.TOWN_NAME,
    )
    try:
        session.add(db_address)
        session.commit()
        session.refresh(db_address)
    except IntegrityError:
        session.rollback()
    return db_address


def process_chunk(session: Session, chunk: pd.DataFrame) -> None:
    """Process a chunk of the data."""
    for _, row in chunk.iterrows():
        address = AddressCreate(**row)
        create_address(session, address)


def drop_table(engine: Engine) -> None:
    """Drop the addressbase table if it exists."""
    Base.metadata.drop_all(engine, tables=[Address.__table__])
