#!/usr/bin/env python3
import json

with open("analysis/literature_search_results.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for tag, res in data.items():
    print(f"\n==================== {tag} ====================")
    for p in res.get("europe_pmc", []):
        print(f"[EPMC] Title: {p.get('title')}")
        print(f"       Authors: {p.get('authors')}")
        print(f"       DOI: {p.get('doi')} | PMID: {p.get('pmid')} | Year: {p.get('pub_year')}")
    for p in res.get("crossref", []):
        print(f"[CR]   Title: {p.get('title')}")
        print(f"       Authors: {p.get('authors')}")
        print(f"       DOI: {p.get('doi')} | Year: {p.get('pub_year')}")
