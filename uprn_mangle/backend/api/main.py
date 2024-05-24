"""This contains the API for the UPRN Mangle service."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any

import uvicorn
from fastapi import FastAPI
from fastapi_pagination import add_pagination

from uprn_mangle.backend.api.routes import router
from uprn_mangle.backend.database import init_models


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:  # noqa: ARG001
    """Run tasks before and after the server starts."""
    await init_models()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(router, prefix="/api/v2")

add_pagination(app)

if __name__ == "__main__":
    uvicorn.run("uprn_mangle.backend.api.main:app", reload=True)