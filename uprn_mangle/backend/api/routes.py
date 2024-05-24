"""Define the API routes for the application."""

from collections.abc import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from uprn_mangle.backend.database import get_db
from uprn_mangle.backend.models import Address
from uprn_mangle.backend.schemas import UPRNResponse

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint to Check API functionality."""
    return {"message": "UPRN Database API Access functional."}


@router.get("/search", response_model=Sequence[UPRNResponse])
async def search(
    q: str, session: AsyncSession = Depends(get_db)
) -> Sequence[UPRNResponse]:
    """Search for an address in the UPRN database.

    Returns a list of addresses that match the search term.
    """
    results = await session.execute(
        select(Address).where(Address.FULL_ADDRESS.ilike(f"%{q}%"))
    )

    return results.scalars().all()
