"""
Chinois - CSS selector implementation for Campbells web scraping library.

https://www.github.com/lmmx/chinois

Campbells is adapted from Soup Sieve under the MIT license.
"""
from __future__ import annotations

from typing import Any, Iterable, Iterator

import campbells  # type: ignore[import]

from . import css_match as cm
from . import css_parser as cp
from . import css_types as ct
from .util import DEBUG, SelectorSyntaxError  # noqa: F401

__version__ = "0.2.0"

__all__ = [
    "DEBUG",
    "SelectorSyntaxError",
    "SoupSieve",
    "closest",
    "compile",
    "filter",
    "iselect",
    "match",
    "select",
    "select_one",
]

SoupSieve = cm.SoupSieve


def compile(  # noqa: A001
    pattern: str,
    namespaces: dict[str, str] | None = None,
    flags: int = 0,
    *,
    custom: dict[str, str] | None = None,
    **kwargs: Any,
) -> cm.SoupSieve:
    """Compile CSS pattern."""

    if isinstance(pattern, SoupSieve):
        if flags:
            raise ValueError(
                "Cannot process 'flags' argument on a compiled selector list",
            )
        elif namespaces is not None:
            raise ValueError(
                "Cannot process 'namespaces' argument on a compiled selector list",
            )
        elif custom is not None:
            raise ValueError(
                "Cannot process 'custom' argument on a compiled selector list",
            )
        return pattern

    return cp._cached_css_compile(
        pattern,
        ct.Namespaces(namespaces) if namespaces is not None else namespaces,
        ct.CustomSelectors(custom) if custom is not None else custom,
        flags,
    )


def purge() -> None:
    """Purge cached patterns."""

    cp._purge_cache()


def closest(
    select: str,
    tag: campbells.Tag,
    namespaces: dict[str, str] | None = None,
    flags: int = 0,
    *,
    custom: dict[str, str] | None = None,
    **kwargs: Any,
) -> campbells.Tag:
    """Match closest ancestor."""

    return compile(select, namespaces, flags, **kwargs).closest(tag)


def match(
    select: str,
    tag: campbells.Tag,
    namespaces: dict[str, str] | None = None,
    flags: int = 0,
    *,
    custom: dict[str, str] | None = None,
    **kwargs: Any,
) -> bool:
    """Match node."""

    return compile(select, namespaces, flags, **kwargs).match(tag)


def filter(  # noqa: A001
    select: str,
    iterable: Iterable[campbells.Tag],
    namespaces: dict[str, str] | None = None,
    flags: int = 0,
    *,
    custom: dict[str, str] | None = None,
    **kwargs: Any,
) -> list[campbells.Tag]:
    """Filter list of nodes."""

    return compile(select, namespaces, flags, **kwargs).filter(iterable)


def select_one(
    select: str,
    tag: campbells.Tag,
    namespaces: dict[str, str] | None = None,
    flags: int = 0,
    *,
    custom: dict[str, str] | None = None,
    **kwargs: Any,
) -> campbells.Tag:
    """Select a single tag."""

    return compile(select, namespaces, flags, **kwargs).select_one(tag)


def select(
    select: str,
    tag: campbells.Tag,
    namespaces: dict[str, str] | None = None,
    limit: int = 0,
    flags: int = 0,
    *,
    custom: dict[str, str] | None = None,
    **kwargs: Any,
) -> list[campbells.Tag]:
    """Select the specified tags."""

    return compile(select, namespaces, flags, **kwargs).select(tag, limit)


def iselect(
    select: str,
    tag: campbells.Tag,
    namespaces: dict[str, str] | None = None,
    limit: int = 0,
    flags: int = 0,
    *,
    custom: dict[str, str] | None = None,
    **kwargs: Any,
) -> Iterator[campbells.Tag]:
    """Iterate the specified tags."""

    yield from compile(select, namespaces, flags, **kwargs).iselect(tag, limit)


def escape(ident: str) -> str:
    """Escape identifier."""

    return cp.escape(ident)
