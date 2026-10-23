"""Source registrations.

Importing this package registers every source in the global registry. Each
entry maps a legacy async crawler function to a :class:`~osintkit.core.Source`
via :class:`~osintkit.core.FunctionSource`, declaring the indicator kind it
accepts and the environment variables (if any) that unlock it.
"""
from ..core import FunctionSource, register

from .adverse_media import search_adverse_media
from .censys import search_hosts as censys_search_hosts, get_host as censys_get_host
from .companies_house import search_companies_house, companies_house_company
from .court_records import search_court_records
from .dehashed import search as dehashed_search
from .emailrep import check_email_rep
from .etherscan import trace_eth_address
from .geocode import geocode, reverse_geocode
from .google_dorks import run_dork
from .hunter import hunt_domain_emails
from .ipinfo import enrich_ip_ipinfo
from .mailaccess import enrich_email_mailaccess
from .maritime import track_vessel
from .otx import enrich_otx
from .reddit import reddit_search, reddit_user
from .sanctions import check_sanctions
from .torbot import crawl_onion_torbot
from .voidaccess import crawl_voidaccess
from .whois_history import get_whois_history
from .wigle import enrich_wifi_wigle
from .wikidata import lookup_wikidata


def _register_all() -> None:
    register(FunctionSource(
        "adverse_media", search_adverse_media, kind="name",
        description="Negative-news screening by scraping public news search."))
    register(FunctionSource(
        "censys", censys_search_hosts, kind="query",
        env_keys=("CENSYS_API_ID", "CENSYS_API_SECRET"),
        description="Internet host/certificate search (Censys).",
        extra_ops={"get_host": censys_get_host}))
    register(FunctionSource(
        "companies_house", search_companies_house, kind="company",
        env_keys=("COMPANIES_HOUSE_KEY",),
        description="UK company registry: officers, PSC/beneficial ownership, filings.",
        extra_ops={"company": companies_house_company}))
    register(FunctionSource(
        "court_records", search_court_records, kind="name",
        description="US court / PACER-style docket search (public sources)."))
    register(FunctionSource(
        "dehashed", dehashed_search, kind="query",
        env_keys=("DEHASHED_EMAIL", "DEHASHED_KEY"),
        description="Breach-credential search (DeHashed)."))
    register(FunctionSource(
        "emailrep", check_email_rep, kind="email",
        description="Email reputation & profile (EmailRep.io). Optional EMAILREP_KEY raises limits."))
    register(FunctionSource(
        "etherscan", trace_eth_address, kind="wallet",
        env_keys=("ETHERSCAN_API_KEY",),
        description="Ethereum balance + transaction trace (Etherscan)."))
    register(FunctionSource(
        "geocode", geocode, kind="query",
        description="Forward geocoding via OpenStreetMap Nominatim (keyless).",
        extra_ops={"reverse": reverse_geocode}))
    register(FunctionSource(
        "google_dorks", run_dork, kind="query",
        env_keys=("GOOGLE_CSE_CX", "GOOGLE_CSE_KEY"),
        description="Google dork queries via Custom Search JSON API."))
    register(FunctionSource(
        "hunter", hunt_domain_emails, kind="domain",
        env_keys=("HUNTER_API_KEY",),
        description="Email discovery for a domain (Hunter.io)."))
    register(FunctionSource(
        "ipinfo", enrich_ip_ipinfo, kind="ip",
        description="IP geolocation / ASN / org (IPinfo). Optional IPINFO_TOKEN raises limits."))
    register(FunctionSource(
        "mailaccess", enrich_email_mailaccess, kind="email",
        env_keys=("MAILACCESS_API_KEY", "MAILACCESS_URL"),
        description="Email account/deliverability checks via a self-hosted MailAccess service."))
    register(FunctionSource(
        "maritime", track_vessel, kind="query",
        description="Vessel / ship tracking by name or IMO/MMSI (keyless)."))
    register(FunctionSource(
        "otx", enrich_otx, kind="query",
        env_keys=("OTX_API_KEY",),
        description="AlienVault OTX threat intel for an IP / domain / hash."))
    register(FunctionSource(
        "reddit", reddit_search, kind="query",
        env_keys=("REDDIT_CLIENT_ID", "REDDIT_CLIENT_SECRET"),
        description="Reddit post search and user lookup.",
        extra_ops={"user": reddit_user}))
    register(FunctionSource(
        "sanctions", check_sanctions, kind="name",
        description="Sanctions / PEP screening against OFAC, EU and UN lists (keyless)."))
    register(FunctionSource(
        "torbot", crawl_onion_torbot, kind="onion",
        env_keys=("TORBOT_URL",),
        description="Crawl a .onion URL via a self-hosted TorBot service."))
    register(FunctionSource(
        "voidaccess", crawl_voidaccess, kind="query",
        env_keys=("VOIDACCESS_URL",),
        description="Dark-web search via a self-hosted VoidAccess service."))
    register(FunctionSource(
        "whois_history", get_whois_history, kind="domain",
        env_keys=("VIEWDNS_KEY",),
        description="Historical WHOIS records for a domain (ViewDNS)."))
    register(FunctionSource(
        "wigle", enrich_wifi_wigle, kind="wifi",
        env_keys=("WIGLE_API_KEY",),
        description="Wi-Fi BSSID/SSID geolocation (WiGLE)."))
    register(FunctionSource(
        "wikidata", lookup_wikidata, kind="query",
        description="Entity lookup against Wikidata (keyless)."))


_register_all()
