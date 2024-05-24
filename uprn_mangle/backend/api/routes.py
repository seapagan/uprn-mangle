"""Define the API routes for the application."""

from collections.abc import Sequence
from typing import Any

from fastapi import APIRouter, Depends
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination.links import Page
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from uprn_mangle.backend.database import get_db
from uprn_mangle.backend.models import Address
from uprn_mangle.backend.schemas import UPRNResponse

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint to Check API functionality."""
    return {"message": "UPRN Database API Access functional."}


@router.get("/search", response_model=Page[UPRNResponse])
async def search(
    q: str, session: AsyncSession = Depends(get_db)
) -> Sequence[Address]:
    """Search for an address in the UPRN database.

    Returns a list of addresses that match the search term.
    """
    query = select(Address).where(
        Address.TSV.op("@@")(func.plainto_tsquery("english", q))
    )

    return await paginate(session, query)
