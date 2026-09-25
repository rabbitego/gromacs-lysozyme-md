#!/usr/bin/env python3
import json

with open("analysis/deep_idp_lit.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for q, res in data.items():
    print(f"\n==================== {q} ====================")
    for p in res.get("epmc", []):
        print(f"[EPMC] Title: {p.get('title')}")
        print(f"       Authors: {p.get('authors')}")
        print(f"       Journal: {p.get('journal')} ({p.get('pub_year')}) | DOI: {p.get('doi')} | PMID: {p.get('pmid')}")
        print(f"       URL: {p.get('url')}")
    for p in res.get("cr", []):
        print(f"[CR]   Title: {p.get('title')}")
        print(f"       Authors: {p.get('authors')}")
        print(f"       DOI: {p.get('doi')} | Year: {p.get('pub_year')}")
