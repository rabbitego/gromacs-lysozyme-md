"""Visualization suite for Rosetta REF2015 Energy Landscape and Enzyme Design Candidates.

Generates high-resolution publication-quality figures:
1. Rosetta REF2015 full energy term weight distribution and physical interpretation.
2. Multi-component energy decomposition across prioritized enzyme mutants.
3. MD-Rosetta dynamic flexibility vs design tolerance correlation.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

# Ensure local module access
sys.path.insert(0, str(Path(__file__).resolve().parent))
from rosetta_engine import LysozymeDesignEngine, REF2015_WEIGHTS


def plot_rosetta_energy_terms(output_dir: Path) -> Path:
    """Generate publication plot of REF2015 scoring function weights."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    terms = [
        r"$fa\_atr$" + "\n(Attractive vdW)",
        r"$fa\_rep$" + "\n(Repulsive vdW)",
        r"$fa\_sol$" + "\n(EEF1 Solvation)",
        r"$fa\_elec$" + "\n(Electrostatics)",
        r"$hbond\_sc$" + "\n(SC-SC H-bonds)",
        r"$hbond\_bb\_sc$" + "\n(BB-SC H-bonds)",
        r"$rama\_prepro$" + "\n(Ramachandran)",
        r"$fa\_dun$" + "\n(Rotamers)",
        r"$p\_aa\_pp$" + "\n(AA Probability)",
    ]
    
    weights = list(REF2015_WEIGHTS.values())
    colors = ["#2b5c8f", "#d95f02", "#7570b3", "#1b9e77", "#e7298a", "#e6ab02", "#a6761d", "#666666", "#1f78b4"]

    fig, ax = plt.subplots(figsize=(10, 5.2), dpi=300)
    bars = ax.bar(terms, weights, color=colors, edgecolor="black", width=0.6, linewidth=0.8, alpha=0.9)
    
    ax.set_ylabel("REF2015 Relative Term Weight", fontsize=11, fontweight="bold")
    ax.set_title("Standard Rosetta Energy Function (REF2015) Term Weights & Energy Decomposition", fontsize=13, fontweight="bold", pad=12)
    ax.set_ylim(0, 1.25)
    ax.grid(axis="y", linestyle=":", alpha=0.6)

    for bar in bars:
        height = bar.get_height()
        ax.annotate(f"{height:.3f}",
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 4),
                    textcoords="offset points",
                    ha="center", va="bottom", fontsize=9, fontweight="bold")

    plt.xticks(rotation=20, ha="right", fontsize=9.5)
    plt.tight_layout()
    
    out_path = output_dir / "rosetta_energy_terms.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    return out_path


def plot_md_vs_design_flexibility(output_dir: Path, md_json_path: Path) -> Path:
    """Plots residue RMSF against mutational position and tolerance."""
    output_dir.mkdir(parents=True, exist_ok=True)
    engine = LysozymeDesignEngine(md_stats_path=md_json_path if md_json_path.exists() else None)
    evals = engine.build_research_library()

    fig, ax = plt.subplots(figsize=(9, 5.5), dpi=300)
    
    positions = [c.position for c in evals]
    rmsfs = [c.rmsf_nm * 10.0 for c in evals]  # Convert nm to Angstrom
    ddg_folds = [c.ddg_fold_reu for c in evals]
    labels = [f"{c.variant_id} ({c.wild_type}{c.position}{c.mutant})" for c in evals]

    sc = ax.scatter(rmsfs, ddg_folds, s=150, c=ddg_folds, cmap="coolwarm", edgecolors="black", linewidth=1.2, zorder=5)
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label(r"$\Delta\Delta G_{fold}$ (REU)", fontweight="bold")

    for i, txt in enumerate(labels):
        ax.annotate(txt, (rmsfs[i], ddg_folds[i]), xytext=(6, 4), textcoords="offset points", fontsize=8.5, fontweight="bold")

    ax.axhline(0, color="black", linestyle="--", linewidth=1.0)
    ax.set_xlabel(r"MD-Derived Local Backbone Flexibility (C$\alpha$ RMSF, $\AA$)", fontsize=11, fontweight="bold")
    ax.set_ylabel(r"Predicted Folding Free Energy Change $\Delta\Delta G_{fold}$ (REU)", fontsize=11, fontweight="bold")
    ax.set_title("MD Conformational Flexibility vs Rosetta Mutational Stability", fontsize=13, fontweight="bold", pad=12)
    ax.grid(True, linestyle=":", alpha=0.6)

    plt.tight_layout()
    out_path = output_dir / "md_vs_rosetta_flexibility.png"
    plt.savefig(out_path, dpi=300, bbox_inches="tight")
    plt.close()
    return out_path


if __name__ == "__main__":
    workspace = Path(__file__).resolve().parent.parent.parent
    figures_path = workspace / "rosetta_learning" / "figures"
    md_json = workspace / "analysis" / "md_statistical_validation.json"

    p1 = plot_rosetta_energy_terms(figures_path)
    engine = LysozymeDesignEngine(md_stats_path=md_json)
    evals = engine.build_research_library()
    engine.generate_research_plots(evals, figures_path)
    p3 = plot_md_vs_design_flexibility(figures_path, md_json)
    print(f"Generated research visual assets in {figures_path}")

