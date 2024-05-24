"""Define the API routes for the application."""

from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def root() -> dict[str, str]:
    """Root endpoint to Check API functionality."""
    return {"message": "UPRN Database API Access functional."}


@router.get("/search")
def search(q: str) -> dict[str, str]:
    """Search for an address in the UPRN database.

    Returns a list of addresses that match the search term.
    """
    return {
        "message": "UPRN Database API Access functional.",
        "Search term": q.strip(),
    }
