"""Research-grade utilities and data models for Rosetta Enzyme Design & Engineering.

Organizes structural, sequence, and energy-based reasoning around rational enzyme engineering,
providing programmatic interfaces for scoring, ranking, and integrating with molecular dynamics.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np


@dataclass
class MutationCandidate:
    """Represents a targeted point substitution with structural and biophysical rationale."""
    position: int
    wild_type: str
    mutant: str
    rationale: str
    structural_context: str
    subsite: str = "Active Cleft"
    predicted_ddg_reu: float = 0.0
    catalytic_score: float = 1.0
    confidence: str = "medium"
    notes: List[str] = field(default_factory=list)

    def summary(self) -> str:
        return (
            f"Pos {self.position:3d}: {self.wild_type}->{self.mutant} | "
            f"Subsite: {self.subsite:<12} | ddG: {self.predicted_ddg_reu:+.2f} REU | "
            f"CatScore: {self.catalytic_score:.2f} | Confidence: {self.confidence} | "
            f"Rationale: {self.rationale}"
        )


def rank_mutation_candidates(
    candidates: List[MutationCandidate],
    weight_stability: float = 0.5,
    weight_binding: float = 0.3,
    weight_catalytic: float = 0.2
) -> List[MutationCandidate]:
    """Multi-objective ranking function balancing stability, activity, and catalytic conservation.

    Args:
        candidates: List of design candidates.
        weight_stability: Importance weight for folding free energy (lower is better).
        weight_binding: Importance weight for subsite engagement.
        weight_catalytic: Penalty weight against perturbing catalytic geometry.

    Returns:
        Sorted list of candidate designs ranked by fitness.
    """
    def composite_fitness(c: MutationCandidate) -> float:
        # Negative ddG is favorable; catalytic score near 1.0 is favorable
        score = -c.predicted_ddg_reu * weight_stability
        if c.catalytic_score < 0.5:
            score -= 50.0  # Severe penalty for catalytic inactivation
        score += c.catalytic_score * 10.0 * weight_catalytic
        if c.confidence == "high":
            score += 2.0
        elif c.confidence == "low":
            score -= 2.0
        return score

    return sorted(candidates, key=composite_fitness, reverse=True)


def generate_design_report(target_name: str, objective: str, candidates: List[MutationCandidate]) -> str:
    """Formats a structured research-level design report."""
    ranked = rank_mutation_candidates(candidates)
    lines = [
        "=" * 80,
        f"  RATIONAL ENZYME DESIGN REPORT: {target_name.upper()}",
        "=" * 80,
        f"Objective: {objective}",
        f"Total Candidates Evaluated: {len(candidates)}",
        "-" * 80,
        "RANKED MUTATIONAL CANDIDATES (Multi-Objective Optimization):",
    ]

    for idx, c in enumerate(ranked, start=1):
        lines.append(f"  {idx:2d}. {c.summary()}")

    lines.extend([
        "-" * 80,
        "BIOPHYSICAL INTERPRETATION & RECOMMENDATIONS:",
        "1. Prioritize Pareto-optimal designs located at subsite periphery (Subsites A, B, E).",
        "2. Strictly enforce catalytic dyad geometry (Glu35 / Asp52 invariant constraints).",
        "3. Pair candidate expression with experimental validation (nanoDSF Tm & kinetic assays).",
        "=" * 80,
    ])
    return "\n".join(lines)


# Backwards compatibility alias
design_brief = generate_design_report


if __name__ == "__main__":
    from rosetta_engine import LysozymeDesignEngine
    engine = LysozymeDesignEngine()
    evaluated = engine.build_research_library()
    
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
            notes=[e.risk_assessment],
        )
        for e in evaluated
    ]
    
    print(generate_design_report(
        target_name="Hen Egg-White Lysozyme (HEWL, 1AKI)",
        objective="Subsite specificity tuning and substrate cleft remodeling while preserving catalytic acid/base machinery",
        candidates=candidates,
    ))

