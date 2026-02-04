"""Customized pagination for the Address model."""

from typing import TypeVar

from fastapi_pagination.customization import (
    CustomizedPage,
    UseFieldsAliases,
    UseParamsFields,
)
from fastapi_pagination.default import Page
from fastapi_pagination.links import UseLinks

T = TypeVar("T")


Pagination = CustomizedPage[
    Page[T],
    UseLinks(only_path=False),
    UseParamsFields(size=20),
    UseFieldsAliases(items="addresses"),
]
