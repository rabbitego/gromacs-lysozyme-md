#!/usr/bin/env python3
"""
Comprehensive Literature Scanner for IDP Diffusion Models
"""

import json
from pathlib import Path
from search_scientific_literature import search_europe_pmc, search_pubmed, search_crossref, search_arxiv


QUERIES = [
    ("FoldingDiff", "FoldingDiff protein torsion angle diffusion"),
    ("Torsional_Diffusion", "torsional diffusion protein molecular"),
    ("IDP_Conformational_Ensemble_Diffusion", "diffusion model intrinsically disordered protein conformational ensemble"),
    ("IDP_Generative_Models", "generative model intrinsically disordered protein ensemble PED"),
    ("Protein_Ensemble_Database_ML", "Protein Ensemble Database generative model machine learning"),
    ("EigenFold_Ensemble", "EigenFold generative protein structure diffusion"),
    ("Torsion_Space_Protein_Diffusion", "protein backbone torsion angle diffusion model phi psi"),
    ("Experimental_Validation_IDP", "intrinsically disordered protein ensemble validation SAXS NMR chemical shift"),
    ("idpGAN_idpDiff", "idpGAN OR idpDiff OR Str2IDP OR 'disordered protein' generative"),
    ("AlphaFold_Ensemble_IDP", "AlphaFold conformational ensemble intrinsically disordered"),
]


def run_scans():
    all_results = {}
    for tag, q in QUERIES:
        print(f"=== Running query: {tag} ({q}) ===")
        epmc = search_europe_pmc(q, 5)
        crossref = search_crossref(q, 5)
        arxiv = search_arxiv(q, 5)
        
        all_results[tag] = {
            "query": q,
            "europe_pmc": epmc,
            "crossref": crossref,
            "arxiv": arxiv,
        }

    out_file = Path("analysis/literature_search_results.json")
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2)
    print(f"Results written to {out_file}")


if __name__ == "__main__":
    run_scans()
