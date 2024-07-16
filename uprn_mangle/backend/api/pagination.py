"""Customized pagination for the Address model."""

from typing import TypeVar

from fastapi import Request
from fastapi_pagination.customization import (
    CustomizedPage,
    UseFieldsAliases,
    UseParamsFields,
)
from fastapi_pagination.links import Page
from fastapi_pagination.links.bases import Links

T = TypeVar("T")


Pagination = CustomizedPage[
    Page[T],
    UseParamsFields(size=20),
    UseFieldsAliases(items="addresses"),
]


def fix_links(request: Request, links: Links) -> Links:
    """Fix the links to add the correct base URL."""
    base_url = str(request.base_url).rstrip("/")
    for attr in [
        "next",
        "prev",
        "first",
        "last",
        "self",
    ]:
        link = getattr(links, attr)
        if link:
            setattr(links, attr, f"{base_url}{link}")

    return links
