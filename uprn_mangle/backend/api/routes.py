"""Define the API routes for the application."""

from typing import Annotated

from fastapi import APIRouter, Depends, Request
from fastapi.responses import JSONResponse
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from uprn_mangle.backend.api.pagination import Pagination, fix_links
from uprn_mangle.backend.database import get_db
from uprn_mangle.backend.models import Address
from uprn_mangle.backend.schemas import UPRNResponse

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint to Check API functionality."""
    return {"message": "UPRN Database API Access functional."}


@router.get("/search", response_model=Pagination[UPRNResponse])
async def search(
    request: Request,
    session: Annotated[AsyncSession, Depends(get_db)],
    q: str | None = None,
) -> Pagination[UPRNResponse] | JSONResponse:
    """Search for an address in the UPRN database.

    Returns a list of addresses that match the search term.
    """
    if not q or q.strip() == "":
        return JSONResponse(
            status_code=400, content={"message": "No search term provided."}
        )

    query = select(Address).where(
        Address.tsv.op("@@")(func.plainto_tsquery("english", q))
    )

    page_result: Pagination[UPRNResponse] = await paginate(session, query)
    page_result.links = fix_links(request, page_result.links)

    return page_result
