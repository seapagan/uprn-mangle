"""This contains the API for the UPRN Mangle service."""

from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any
from urllib.parse import urlparse

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import add_pagination

from uprn_mangle.backend.api.routes import router
from uprn_mangle.backend.config import get_settings
from uprn_mangle.backend.database import init_models

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[Any, None]:  # noqa: ARG001
    """Run tasks before and after the server starts."""
    await init_models()
    yield


origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:4173",
]

app = FastAPI(
    lifespan=lifespan, swagger_ui_parameters={"defaultModelsExpandDepth": 0}
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.api_prefix)


add_pagination(app)

if __name__ == "__main__":
    host = urlparse(settings.api_base_url).hostname
    if not host:
        msg = "Bad api_base_url setting, please check the config.toml file."
        raise SystemExit(msg)
    uvicorn.run(
        "uprn_mangle.backend.api.main:app",
        reload=True,
        port=settings.api_port,
        host=host,
    )
