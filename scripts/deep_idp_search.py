#!/usr/bin/env python3
"""
Deep Literature Search on IDP Generative & Diffusion Models
"""

import json
from search_scientific_literature import search_europe_pmc, search_crossref


SPECIFIC_QUERIES = [
    "FoldingDiff protein generation via torsion angle diffusion",
    "Janson Feig Transferable deep generative modeling of intrinsically disordered protein conformations",
    "Protein Ensemble Database conformational ensemble intrinsically disordered",
    "diffusion model conformational ensemble intrinsically disordered protein",
    "AlphaFold intrinsically disordered proteins ensemble Schnapka Bonomi",
    "torsional score-based diffusion model protein",
    "generating structural ensembles of intrinsically disordered proteins",
    "IDPEnsembleTools conformational ensembles disordered proteins",
]

results = {}
for q in SPECIFIC_QUERIES:
    print(f"Fetching: {q}")
    epmc = search_europe_pmc(q, 3)
    cr = search_crossref(q, 3)
    results[q] = {"epmc": epmc, "cr": cr}

with open("analysis/deep_idp_lit.json", "w", encoding="utf-8") as f:
    json.dump(results, f, indent=2)
print("Saved to analysis/deep_idp_lit.json")
