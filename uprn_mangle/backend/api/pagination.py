"""Customized pagination for the Address model."""
from typing import TypeVar

from fastapi_pagination.customization import (
    CustomizedPage,
    UseFieldsAliases,
    UseParamsFields,
)
from fastapi_pagination.links import Page

T = TypeVar("T")


Pagination = CustomizedPage[
    Page[T], UseParamsFields(size=20), UseFieldsAliases(items="addresses")
]
