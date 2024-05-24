"""This contains the API for the UPRN Mangle service."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI

from uprn_mangle.backend.database.db import init_models


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:  # noqa: ARG001
    """Run tasks before and after the server starts."""
    await init_models()
    yield


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root() -> dict[str, str]:
    """Root endpoint to Check API functionality."""
    return {"message": "UPRN Database API Access functional."}


if __name__ == "__main__":
    uvicorn.run("api:app", reload=True)
