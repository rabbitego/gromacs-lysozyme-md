"""Research-grade design brief and pipeline for Hen Egg-White Lysozyme (HEWL).

Integrates subsite-specific structural mechanics, Rosetta REF2015 energy terms,
and thermodynamic validation for engineering carbohydrate active sites.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Add parent directory to path to enable local imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rosetta_engine import LysozymeDesignEngine, MutantEvaluation
from rosetta_learning import MutationCandidate, generate_design_report


def run_lysozyme_design_brief() -> str:
    """Executes the full computational design ranking and produces a research brief."""
    workspace = Path(__file__).resolve().parent.parent.parent
    md_json = workspace / "analysis" / "md_statistical_validation.json"

    engine = LysozymeDesignEngine(md_stats_path=md_json if md_json.exists() else None)
    evaluations = engine.build_research_library()

    candidates = [
        MutationCandidate(
            position=e.position,
            wild_type=e.wild_type,
            mutant=e.mutant,
            rationale=e.rationale,
            structural_context=e.subsite_role,
            subsite=e.target_subsite,
            predicted_ddg_reu=e.ddg_fold_reu,
            catalytic_score=e.catalytic_integrity_score,
            confidence="high" if e.is_pareto_optimal else "medium",
            notes=[f"Role: {e.subsite_role}", f"Risk: {e.risk_assessment}", f"Tier: {e.recommendation_tier}"],
        )
        for e in evaluations
    ]

    report = generate_design_report(
        target_name="Hen Egg-White Lysozyme (HEWL, 1AKI / 1HEW, EC 3.2.1.17)",
        objective="Rational engineering of substrate subsites (A-F) to modulate glycan specificity without disturbing catalytic acid/base machinery (Glu35/Asp52)",
        candidates=candidates,
    )
    return report


if __name__ == "__main__":
    print(run_lysozyme_design_brief())

