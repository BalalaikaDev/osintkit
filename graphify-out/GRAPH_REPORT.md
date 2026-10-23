# Graph Report - osintkit  (2026-10-23)

## Corpus Check
- 28 files · ~9,912 words
- Verdict: corpus is large enough that graph structure adds value.
- Unclassified: 2 file(s) not represented in the graph (top: (none) 2)

## Summary
- 204 nodes · 440 edges · 20 communities (11 shown, 9 thin omitted)
- Extraction: 94% EXTRACTED · 6% INFERRED · 0% AMBIGUOUS · INFERRED: 25 edges (avg confidence: 0.86)
- Token cost: 0 input · 0 output

## Graph Freshness
- Built from commit: `bb46af0e`
- Run `git rev-parse HEAD` and compare to check if the graph is stale.
- Run `graphify update .` after code changes (no API cost).

## Community Hubs (Navigation)
- core.py
- sanctions.py
- os
- reddit.py
- otx.py
- mailaccess.py
- httpx
- voidaccess.py
- _register_all
- sources/__init__.py
- censys.py
- maritime.py
- wigle.py
- wikidata.py
- osintkit
- logging
- google_dorks.py
- whois_history.py
- osintkit

## God Nodes (most connected - your core abstractions)
1. `_register_all()` - 25 edges
2. `Source` - 13 edges
3. `enrich_email_mailaccess()` - 11 edges
4. `SourceResult` - 9 edges
5. `FunctionSource` - 8 edges
6. `trace_eth_address()` - 8 edges
7. `track_vessel()` - 8 edges
8. `reddit_user()` - 8 edges
9. `reddit_search()` - 8 edges
10. `crawl_voidaccess()` - 8 edges

## Surprising Connections (you probably didn't know these)
- `The interface` --references--> `Source`  [INFERRED]
  README.md → osintkit/core.py
- `test_every_source_has_metadata()` --uses--> `Source`  [INFERRED]
  tests/test_registry.py → osintkit/core.py
- `test_result_ok_semantics()` --calls--> `SourceResult`  [EXTRACTED]
  tests/test_registry.py → osintkit/core.py
- `_register_all()` --indirect_call--> `search_adverse_media()`  [INFERRED]
  osintkit/sources/__init__.py → osintkit/sources/adverse_media.py
- `_register_all()` --indirect_call--> `search_court_records()`  [INFERRED]
  osintkit/sources/__init__.py → osintkit/sources/court_records.py

## Import Cycles
- None detected.

## Communities (20 total, 9 thin omitted)

### Community 0 - "core.py"
Cohesion: 0.08
Nodes (12): all_sources(), by_kind(), FunctionSource, get(), kinds(), register(), Source, SourceResult (+4 more)

### Community 1 - "sanctions.py"
Cohesion: 0.14
Nodes (9): _classify_article(), _parse_results(), search_adverse_media(), check_sanctions(), _ensure_loaded(), _fetch_csv(), _load_lists(), _score() (+1 more)

### Community 2 - "os"
Cohesion: 0.17
Nodes (7): _creds(), search(), _eth(), trace_eth_address(), _ts(), _base_url(), crawl_onion_torbot()

### Community 3 - "reddit.py"
Cohesion: 0.24
Nodes (6): _auth_note(), _client_and_base(), _get_token(), reddit_search(), reddit_user(), _ts()

### Community 4 - "otx.py"
Cohesion: 0.25
Nodes (4): enrich_ip_ipinfo(), _is_private(), _classify(), enrich_otx()

### Community 5 - "mailaccess.py"
Cohesion: 0.27
Nodes (6): _base_url(), enrich_email_mailaccess(), _headers(), _is_finished(), _len(), _normalize()

### Community 7 - "voidaccess.py"
Cohesion: 0.31
Nodes (4): _base_url(), crawl_voidaccess(), _summarize(), _top_entities()

### Community 8 - "_register_all"
Cohesion: 0.36
Nodes (4): _auth(), companies_house_company(), search_companies_house(), _register_all()

### Community 10 - "censys.py"
Cohesion: 0.38
Nodes (3): _creds(), get_host(), search_hosts()

### Community 11 - "maritime.py"
Cohesion: 0.43
Nodes (4): _classify(), track_vessel(), _tracking_links(), _ts_ms()

### Community 14 - "osintkit"
Cohesion: 0.33
Nodes (5): Install, Legal / responsible use, License, osintkit, Sources

## Knowledge Gaps
- **1 isolated node(s):** `osintkit`
  These have ≤1 connection - possible missing edges or undocumented components. (Counts symbols only; 92 node(s) total have ≤1 connection when file, concept and rationale nodes are included.)
- **9 thin communities (<3 nodes) omitted from report** — run `graphify query` to explore isolated nodes.

## Suggested Questions
_Questions this graph is uniquely positioned to answer:_

- **Why does `The interface` connect `core.py` to `osintkit`?**
  _High betweenness centrality (0.057) - this node is a cross-community bridge._
- **Are the 22 inferred relationships involving `_register_all()` (e.g. with `search_adverse_media()` and `companies_house_company()`) actually correct?**
  _`_register_all()` has 22 INFERRED edges - model-reasoned connections that need verification._
- **What connects `osintkit` to the rest of the system?**
  _1 weakly-connected nodes found - possible documentation gaps or missing edges._
- **Should `core.py` be split into smaller, more focused modules?**
  _Cohesion score 0.07804878048780488 - nodes in this community are weakly interconnected._
- **Why does `_register_all()` connect `_register_all` to `core.py`, `sanctions.py`, `os`, `reddit.py`, `otx.py`, `mailaccess.py`, `httpx`, `voidaccess.py`, `sources/__init__.py`, `maritime.py`, `wigle.py`, `wikidata.py`, `logging`, `google_dorks.py`, `whois_history.py`?**
  _High betweenness centrality (0.053) - this node is a cross-community bridge._
- **Are the 2 inferred relationships involving `Source` (e.g. with `The interface` and `test_every_source_has_metadata()`) actually correct?**
  _`Source` has 2 INFERRED edges - model-reasoned connections that need verification._
- **Should `sanctions.py` be split into smaller, more focused modules?**
  _Cohesion score 0.14 - nodes in this community are weakly interconnected._