"""Define the API routes for the application."""

from collections.abc import Sequence
from typing import TypeVar

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from fastapi_pagination.customization import (
    CustomizedPage,
    UseFieldsAliases,
    UseParamsFields,
)
from fastapi_pagination.ext.sqlalchemy import paginate
from fastapi_pagination.links import Page
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from uprn_mangle.backend.database import get_db
from uprn_mangle.backend.models import Address
from uprn_mangle.backend.schemas import UPRNResponse

T = TypeVar("T")

router = APIRouter()

Pagination = CustomizedPage[
    Page[T], UseParamsFields(size=20), UseFieldsAliases(items="addresses")
]


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint to Check API functionality."""
    return {"message": "UPRN Database API Access functional."}


@router.get("/search", response_model=Pagination[UPRNResponse])
async def search(
    q: str | None = None, session: AsyncSession = Depends(get_db)
) -> JSONResponse | Sequence[Address]:
    """Search for an address in the UPRN database.

    Returns a list of addresses that match the search term.
    """
    if not q or q.strip() == "":
        return JSONResponse(
            status_code=400, content={"message": "No search term provided."}
        )

    query = select(Address).where(
        Address.TSV.op("@@")(func.plainto_tsquery("english", q))
    )

    return await paginate(session, query)  # type: ignore[no-any-return]
