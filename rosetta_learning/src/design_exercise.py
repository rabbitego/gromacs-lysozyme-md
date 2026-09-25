"""Educational design exercise for learning Rosetta-style computational reasoning.

Connects structural hypotheses to energy scoring, subsite mechanics, and risk trade-offs.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

# Add current directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent))

from rosetta_learning import MutationCandidate, generate_design_report


def generate_candidate_library() -> list[MutationCandidate]:
    return [
        MutationCandidate(
            position=42,
            wild_type="L",
            mutant="I",
            rationale="Makes the binding pocket slightly more compact and improves packing around a hydrophobic substrate.",
            structural_context="Substrate binding pocket",
            subsite="Subsite C",
            predicted_ddg_reu=-0.85,
            catalytic_score=0.99,
            confidence="medium",
            notes=["Conservative aliphatic substitution", "Low fold perturbation risk"],
        ),
        MutationCandidate(
            position=65,
            wild_type="S",
            mutant="T",
            rationale="Adds a methyl group while maintaining polar hydrogen bonding, optimizing substrate orientation.",
            structural_context="Active site rim",
            subsite="Subsite B",
            predicted_ddg_reu=-1.20,
            catalytic_score=0.99,
            confidence="high",
            notes=["Favored first-pass design", "Check for steric clash"],
        ),
        MutationCandidate(
            position=100,
            wild_type="E",
            mutant="Q",
            rationale="Maintains polarity while removing formal negative charge to alter electrostatic steering.",
            structural_context="Catalytic perimeter",
            subsite="Subsite D",
            predicted_ddg_reu=-0.45,
            catalytic_score=0.95,
            confidence="medium",
            notes=["Requires electrostatic verification", "Subtle polar shift"],
        ),
        MutationCandidate(
            position=134,
            wild_type="A",
            mutant="Y",
            rationale="Adds aromatic bulk for stronger carbohydrate stacking, with potential steric risk at channel mouth.",
            structural_context="Cleft entrance",
            subsite="Subsite A",
            predicted_ddg_reu=+0.60,
            catalytic_score=0.90,
            confidence="low",
            notes=["High-impact design", "Risk of channel occlusion"],
        ),
        MutationCandidate(
            position=201,
            wild_type="N",
            mutant="D",
            rationale="Introduces a carboxylate that enhances electrostatic steering if placed favorably at solvent boundary.",
            structural_context="Outer cleft edge",
            subsite="Subsite E",
            predicted_ddg_reu=-1.10,
            catalytic_score=0.98,
            confidence="high",
            notes=["Biochemically plausible", "Check solvation penalty"],
        ),
    ]


def main() -> None:
    candidates = generate_candidate_library()
    report = generate_design_report(
        target_name="Example Enzyme Scaffold",
        objective="Which substitutions are most promising for tuning substrate specificity while preserving fold stability?",
        candidates=candidates,
    )
    print(report)


if __name__ == "__main__":
    main()

