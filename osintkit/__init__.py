"""osintkit — a uniform interface over free and keyed OSINT data sources.

Each source takes one indicator (an IP, domain, email, name, wallet, …) and
returns a normalized :class:`SourceResult`. Sources are plain async functions
under the hood; the registry gives them one shape and one place to discover them.

    import asyncio
    import osintkit

    async def main():
        src = osintkit.get("ipinfo")
        res = await src.fetch("8.8.8.8")
        print(res.ok, res.data)

        # run every source that accepts a domain
        for s in osintkit.by_kind("domain"):
            if s.configured:
                print(await s.fetch("example.com"))

    asyncio.run(main())
"""
from .core import (
    Source,
    FunctionSource,
    SourceResult,
    register,
    get,
    all_sources,
    by_kind,
    kinds,
)
from . import sources as _sources  # noqa: F401  (import registers all sources)

__version__ = "0.1.0"

__all__ = [
    "Source",
    "FunctionSource",
    "SourceResult",
    "register",
    "get",
    "all_sources",
    "by_kind",
    "kinds",
    "describe",
    "__version__",
]


def describe() -> str:
    """A human-readable table of every registered source and its configuration."""
    rows = []
    for s in all_sources():
        status = "keyless" if s.keyless else ("ready" if s.configured else "needs key")
        keys = ",".join(s.env_keys) if s.env_keys else "-"
        rows.append(f"{s.name:16} {s.kind:9} {status:9} {keys:40} {s.description}")
    header = f"{'SOURCE':16} {'KIND':9} {'STATUS':9} {'ENV KEYS':40} DESCRIPTION"
    return "\n".join([header, *rows])
