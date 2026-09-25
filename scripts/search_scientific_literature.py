#!/usr/bin/env python3
"""
Scientific Literature Retrieval Tool
====================================
Queries NCBI PubMed (e-utilities), Europe PMC REST API, Crossref API, and arXiv API
to retrieve verified primary literature, DOIs, PMIDs, authors, abstracts, and metadata.
"""

import json
import time
import urllib.parse
import urllib.request
from typing import Any, Dict, List, Optional


HEADERS = {
    "User-Agent": "DeepBioResearchAgent/1.0 (mailto:scientific_research_audit@domain.org)"
}


def search_europe_pmc(query: str, page_size: int = 10) -> List[Dict[str, Any]]:
    """Search Europe PMC for peer-reviewed literature and preprints."""
    base_url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    params = {
        "query": query,
        "format": "json",
        "pageSize": str(page_size),
        "resultType": "core",
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            results = data.get("resultList", {}).get("result", [])
            papers = []
            for r in results:
                papers.append({
                    "title": r.get("title"),
                    "authors": r.get("authorString"),
                    "journal": r.get("journalTitle") or r.get("bookOrReportDetails", {}).get("publisher"),
                    "pub_year": r.get("pubYear"),
                    "doi": r.get("doi"),
                    "pmid": r.get("pmid"),
                    "pmcid": r.get("pmcid"),
                    "pub_type": r.get("pubType"),
                    "source": r.get("source"),
                    "abstract": r.get("abstractText"),
                    "url": f"https://doi.org/{r.get('doi')}" if r.get("doi") else f"https://europepmc.org/article/{r.get('source')}/{r.get('id')}",
                })
            return papers
    except Exception as e:
        print(f"Europe PMC search failed for '{query}': {e}")
        return []


def search_pubmed(query: str, retmax: int = 10) -> List[Dict[str, Any]]:
    """Search PubMed via NCBI e-utilities (esearch + esummary)."""
    esearch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    params = {
        "db": "pubmed",
        "term": query,
        "retmode": "json",
        "retmax": str(retmax),
    }
    url = f"{esearch_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            id_list = data.get("esearchresult", {}).get("idlist", [])
            if not id_list:
                return []
    except Exception as e:
        print(f"PubMed search failed: {e}")
        return []

    # Fetch summaries
    esummary_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi"
    sum_params = {
        "db": "pubmed",
        "id": ",".join(id_list),
        "retmode": "json",
    }
    url_sum = f"{esummary_url}?{urllib.parse.urlencode(sum_params)}"
    req_sum = urllib.request.Request(url_sum, headers=HEADERS)
    try:
        with urllib.request.urlopen(req_sum, timeout=15) as resp:
            sum_data = json.loads(resp.read().decode("utf-8"))
            result_dict = sum_data.get("result", {})
            papers = []
            for pmid in id_list:
                item = result_dict.get(pmid, {})
                article_ids = item.get("articleids", [])
                doi = None
                for aid in article_ids:
                    if aid.get("idtype") == "doi":
                        doi = aid.get("value")
                papers.append({
                    "title": item.get("title"),
                    "authors": ", ".join([a.get("name", "") for a in item.get("authors", [])]),
                    "journal": item.get("source"),
                    "pub_year": item.get("pubdate", "")[:4],
                    "doi": doi,
                    "pmid": pmid,
                    "url": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
                })
            return papers
    except Exception as e:
        print(f"PubMed summary fetch failed: {e}")
        return []


def search_crossref(query: str, rows: int = 10) -> List[Dict[str, Any]]:
    """Search Crossref for primary literature and DOIs."""
    base_url = "https://api.crossref.org/works"
    params = {
        "query": query,
        "rows": str(rows),
        "select": "DOI,title,author,published-print,published-online,container-title,abstract,type,is-referenced-by-count",
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            items = data.get("message", {}).get("items", [])
            papers = []
            for it in items:
                authors = []
                for a in it.get("author", []):
                    authors.append(f"{a.get('given', '')} {a.get('family', '')}".strip())
                pub = it.get("published-print") or it.get("published-online") or {}
                year = pub.get("date-parts", [[None]])[0][0]
                papers.append({
                    "title": it.get("title", [""])[0],
                    "authors": ", ".join(authors),
                    "journal": it.get("container-title", [""])[0] if it.get("container-title") else None,
                    "pub_year": year,
                    "doi": it.get("DOI"),
                    "type": it.get("type"),
                    "citations": it.get("is-referenced-by-count"),
                    "abstract": it.get("abstract"),
                    "url": f"https://doi.org/{it.get('DOI')}",
                })
            return papers
    except Exception as e:
        print(f"Crossref search failed: {e}")
        return []


def search_arxiv(query: str, max_results: int = 10) -> List[Dict[str, Any]]:
    """Search arXiv API for preprint papers."""
    base_url = "http://export.arxiv.org/api/query"
    params = {
        "search_query": query,
        "max_results": str(max_results),
        "sortBy": "relevance",
        "sortOrder": "descending",
    }
    url = f"{base_url}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers=HEADERS)
    try:
        import xml.etree.ElementTree as ET
        with urllib.request.urlopen(req, timeout=15) as resp:
            xml_data = resp.read().decode("utf-8")
            root = ET.fromstring(xml_data)
            ns = {"atom": "http://www.w3.org/2005/Atom"}
            papers = []
            for entry in root.findall("atom:entry", ns):
                title = entry.find("atom:title", ns)
                summary = entry.find("atom:summary", ns)
                id_elem = entry.find("atom:id", ns)
                published = entry.find("atom:published", ns)
                authors = [a.find("atom:name", ns).text for a in entry.findall("atom:author", ns) if a.find("atom:name", ns) is not None]
                papers.append({
                    "title": title.text.strip().replace("\n", " ") if title is not None else "",
                    "authors": ", ".join(authors),
                    "pub_year": published.text[:4] if published is not None else None,
                    "abstract": summary.text.strip().replace("\n", " ") if summary is not None else "",
                    "url": id_elem.text if id_elem is not None else None,
                    "journal": "arXiv preprint",
                })
            return papers
    except Exception as e:
        print(f"arXiv search failed: {e}")
        return []


if __name__ == "__main__":
    import sys
    q = sys.argv[1] if len(sys.argv) > 1 else "diffusion models intrinsically disordered protein ensemble"
    print(f"Searching for: {q}\n")
    
    print("=== Europe PMC ===")
    epmc_res = search_europe_pmc(q, 5)
    for p in epmc_res:
        print(f"Title: {p['title']}")
        print(f"Authors: {p['authors']}")
        print(f"Journal: {p['journal']} ({p['pub_year']}) | DOI: {p['doi']} | PMID: {p['pmid']}")
        print(f"URL: {p['url']}")
        print("-" * 60)
