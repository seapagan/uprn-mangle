"""Helper functions used by the main Class."""

import re
from typing import cast

import pandas as pd
from rich import print as rprint
from sqlalchemy import Engine, Table
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.sql.expression import func

from uprn_mangle.backend.database.db import Base
from uprn_mangle.backend.models import Address
from uprn_mangle.backend.schemas import AddressCreate


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


def generate_full_address(address: AddressCreate) -> str:
    """Generate full address by concatenating specific fields."""
    fields = [
        address.sub_building_name.strip(),
        address.building_name.strip(),
        address.building_number.strip(),
        address.thoroughfare.strip(),
        address.post_town.strip(),
        address.postcode.strip(),
        address.administrative_area.strip(),
    ]
    return ", ".join([field for field in fields if field])


def create_address(session: Session, address: AddressCreate) -> Address | None:
    """Create a new address entry in the database."""
    if address.postcode.strip() == "":
        return None  # we don't want to store addresses without a postcode

    full_address = generate_full_address(address)

    db_address = Address(
        uprn=address.uprn,
        full_address=full_address,
        sub_building_name=address.sub_building_name,
        building_name=address.building_name,
        building_number=address.building_number,
        thoroughfare=address.thoroughfare,
        post_town=address.post_town,
        postcode=address.postcode,
        administrative_area=address.administrative_area,
        logical_status=address.logical_status,
        blpu_state=address.blpu_state,
        x_coordinate=address.x_coordinate,
        y_coordinate=address.y_coordinate,
        latitude=address.latitude,
        longitude=address.longitude,
        country=address.country,
        classification_code=address.classification_code,
        usrn=address.usrn,
        street_description=address.street_description,
        locality=address.locality,
        town_name=address.town_name,
        tsv=func.to_tsvector(full_address),
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
    Base.metadata.drop_all(engine, tables=[cast(Table, Address.__table__)])
