"""Helper functions used by the main Class."""

import re
from typing import cast

import pandas as pd
from rich.console import Console
from rich.panel import Panel
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


def show_header(title: str, text_list: list[str]) -> None:
    """Show a header panel using Rich.panel."""
    console = Console(width=80)
    panel = Panel(
        "\n".join(text_list),
        title="[b][blue]UPRN Import[/b]",
        subtitle=f"[blue]{title}",
        title_align="left",
        subtitle_align="left",
        padding=(1, 2),
        style="green",
    )
    console.print(panel)


def generate_full_address(address: AddressCreate) -> str:
    """Generate full address by concatenating specific fields."""
    fields = [
        address.sub_building_name.strip().title(),
        address.building_name.strip().title(),
        address.building_number.strip(),
        address.thoroughfare.strip().title(),
        address.post_town.strip().title(),
        address.postcode.strip(),
        address.administrative_area.strip().title(),
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
        x_coordinate=address.x_coordinate,
        y_coordinate=address.y_coordinate,
        latitude=address.latitude,
        longitude=address.longitude,
        country=address.country,
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
