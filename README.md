# osintkit

A uniform, async interface over free and keyed **OSINT data sources**.

Each source takes a single indicator — an IP, domain, email, name, wallet
address, Wi-Fi BSSID, and so on — and returns a normalized result. Under the
hood every source is a small `async` function that talks to one API; `osintkit`
gives them **one shape, one registry, and one way to discover what's available
and what's configured.**

It was extracted from [runi-os](https://github.com/BalalaikaDev/runi-os), a
self-hosted OSINT platform, so the parsing logic behind each source is the same
code that platform runs in production — this package just puts a clean interface
on top and drops the database coupling, so it stands alone.

```python
import asyncio
import osintkit

async def main():
    # one source
    res = await osintkit.get("ipinfo").fetch("8.8.8.8")
    print(res.ok, res.data)        # -> True {'city': 'Mountain View', 'asn': 'AS15169', ...}

    # every source that accepts a domain, that is actually configured
    for src in osintkit.by_kind("domain"):
        if src.configured:
            print(await src.fetch("example.com"))

asyncio.run(main())
```

## Install

```bash
pip install osintkit          # once published
# or, from a clone:
pip install -e ".[dev]"
```

Requires Python 3.10+. Only runtime dependencies are `httpx` and
`beautifulsoup4`.

## The interface

Every source is a `Source`:

| attribute | meaning |
| --- | --- |
| `name` | stable id, e.g. `"hunter"` |
| `kind` | the indicator it accepts: `ip`, `domain`, `email`, `username`, `phone`, `wallet`, `name`, `company`, `wifi`, `onion`, or `query` |
| `env_keys` | the environment variables that unlock it (empty = keyless) |
| `keyless` | `True` when it needs no configuration |
| `configured` | `True` if keyless, or every declared key is set |

```python
result = await source.fetch(indicator, **opts)
result.ok       # bool: found and no error
result.data     # the source's own dict, unchanged
result.error    # error string, or None
```

Discovery helpers on the package:

```python
osintkit.all_sources()      # every Source, sorted by name
osintkit.get("sanctions")   # one Source by name
osintkit.by_kind("email")   # all Sources that accept an email
osintkit.kinds()            # all indicator kinds in the registry
print(osintkit.describe())  # a readable table of sources + config status
```

## Sources

21 sources across these indicator kinds. Keyless ones work out of the box;
keyed ones read their credentials from environment variables.

| Source | Kind | Keys |
| --- | --- | --- |
| adverse_media | name | *(keyless)* |
| censys | query | `CENSYS_API_ID`, `CENSYS_API_SECRET` |
| companies_house | company | `COMPANIES_HOUSE_KEY` |
| court_records | name | *(keyless)* |
| dehashed | query | `DEHASHED_EMAIL`, `DEHASHED_KEY` |
| emailrep | email | *(optional `EMAILREP_KEY`)* |
| etherscan | wallet | `ETHERSCAN_API_KEY` |
| geocode | query | *(keyless)* |
| google_dorks | query | `GOOGLE_CSE_CX`, `GOOGLE_CSE_KEY` |
| hunter | domain | `HUNTER_API_KEY` |
| ipinfo | ip | *(optional `IPINFO_TOKEN`)* |
| mailaccess | email | `MAILACCESS_API_KEY`, `MAILACCESS_URL` |
| maritime | query | *(keyless)* |
| otx | query | `OTX_API_KEY` |
| reddit | query | `REDDIT_CLIENT_ID`, `REDDIT_CLIENT_SECRET` |
| sanctions | name | *(keyless)* |
| torbot | onion | `TORBOT_URL` |
| voidaccess | query | `VOIDACCESS_URL` |
| whois_history | domain | `VIEWDNS_KEY` |
| wigle | wifi | `WIGLE_API_KEY` |
| wikidata | query | *(keyless)* |

A source with missing keys doesn't crash — it returns a result with
`found=False` and a reason, so you can run a whole batch and let the configured
ones answer.

## Legal / responsible use

These sources query public and commercial intelligence APIs. Use them only
against targets you are authorized to investigate, and respect each provider's
terms of service and rate limits.

## License

MIT © Darius Genkinger
