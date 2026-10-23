"""Core types for osintkit: a uniform interface over heterogeneous OSINT sources.

Every source — whether it hits a free keyless API, a keyed commercial one, or a
self-hosted service — is wrapped as a :class:`Source` with the same shape:

    result = await source.fetch(indicator)
    if result.ok:
        print(result.data)

The sources themselves are plain ``async`` functions that return a ``dict`` (the
historical Fieldwork crawler convention). :class:`FunctionSource` adapts one of
those functions to the :class:`Source` interface without touching its body, so the
parsing logic that was already battle-tested in production is reused verbatim.
"""
from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Awaitable, Callable, Optional


@dataclass
class SourceResult:
    """The normalized return value of every :meth:`Source.fetch` call.

    ``data`` is the source's own dict, unchanged. ``ok`` is the one flag callers
    can rely on across every source regardless of its internal key names.
    """

    source: str
    indicator: str
    found: bool
    data: dict = field(default_factory=dict)
    error: Optional[str] = None

    @property
    def ok(self) -> bool:
        return self.found and self.error is None

    def to_dict(self) -> dict:
        return {
            "source": self.source,
            "indicator": self.indicator,
            "found": self.found,
            "error": self.error,
            "data": self.data,
        }


class Source:
    """Uniform interface over one OSINT data source.

    Attributes
    ----------
    name:        stable identifier, e.g. ``"ipinfo"``.
    kind:        the indicator type it accepts — ``ip``, ``domain``, ``email``,
                 ``username``, ``phone``, ``wallet``, ``name``, ``company``,
                 ``wifi``, ``onion`` or the catch-all ``query``.
    env_keys:    environment variables that unlock (or raise the limits of) the
                 source. Empty means fully keyless.
    keyless:     ``True`` when the source works with no configuration at all.
    description: one line, shown by :func:`osintkit.describe`.
    """

    name: str = ""
    kind: str = "query"
    env_keys: tuple[str, ...] = ()
    keyless: bool = True
    description: str = ""

    async def fetch(self, indicator: str, **opts) -> SourceResult:  # pragma: no cover
        raise NotImplementedError

    @property
    def configured(self) -> bool:
        """True if the source needs no keys, or every declared key is present."""
        if self.keyless:
            return True
        return all(os.getenv(k) for k in self.env_keys)


class FunctionSource(Source):
    """Adapt a legacy ``async def fn(indicator, **opts) -> dict`` to :class:`Source`.

    The wrapped function keeps returning its own dict; we wrap that dict in a
    :class:`SourceResult`, inferring ``found`` from the dict's own ``found`` key
    (falling back to "no error key present").
    """

    def __init__(
        self,
        name: str,
        fn: Callable[..., Awaitable[dict]],
        *,
        kind: str = "query",
        env_keys: tuple[str, ...] = (),
        description: str = "",
        extra_ops: Optional[dict[str, Callable[..., Awaitable[dict]]]] = None,
    ) -> None:
        self.name = name
        self.kind = kind
        self.env_keys = env_keys
        self.keyless = not env_keys
        self.description = description
        self._fn = fn
        #: secondary callables that don't fit the single-indicator ``fetch`` shape
        #: (e.g. ``geocode``'s reverse lookup, ``reddit``'s user lookup).
        self.extra_ops = extra_ops or {}

    async def fetch(self, indicator: str, **opts) -> SourceResult:
        data = await self._fn(indicator, **opts)
        if not isinstance(data, dict):
            data = {"value": data}
        error = data.get("error")
        if "found" in data:
            found = bool(data["found"])
        else:
            found = error is None
        return SourceResult(
            source=self.name,
            indicator=indicator,
            found=found,
            data=data,
            error=error if isinstance(error, str) else (str(error) if error else None),
        )


# ── Registry ────────────────────────────────────────────────────────────────
_REGISTRY: dict[str, Source] = {}


def register(source: Source) -> Source:
    """Add a source to the global registry (idempotent by name)."""
    _REGISTRY[source.name] = source
    return source


def get(name: str) -> Source:
    """Return the source registered under ``name`` (raises ``KeyError`` if absent)."""
    return _REGISTRY[name]


def all_sources() -> list[Source]:
    """Every registered source, sorted by name."""
    return [_REGISTRY[k] for k in sorted(_REGISTRY)]


def by_kind(kind: str) -> list[Source]:
    """Every source that accepts the given indicator ``kind``."""
    return [s for s in all_sources() if s.kind == kind]


def kinds() -> list[str]:
    """All distinct indicator kinds the registry can handle."""
    return sorted({s.kind for s in all_sources()})
