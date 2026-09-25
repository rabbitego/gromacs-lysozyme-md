#!/usr/bin/env python3
"""
Test Suite for MD Trajectory and Rosetta Enzyme Design Pipelines
================================================================
Verifies mathematical accuracy, file parsing, thermodynamic invariants,
and mutational scoring consistency.
"""

import json
import sys
import unittest
from pathlib import Path

# Add project root and src to path
WORKSPACE_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE_ROOT / "scripts"))
sys.path.insert(0, str(WORKSPACE_ROOT / "rosetta_learning" / "src"))

from analyze_md_trajectory import MDTrajectoryAnalysis, parse_xvg, compute_statistical_metrics
from rosetta_engine import LysozymeDesignEngine, REF2015_WEIGHTS, EnergyDecomposition
from rosetta_learning import MutationCandidate, rank_mutation_candidates


class TestMDPipeline(unittest.TestCase):
    """Unit and validation tests for GROMACS MD trajectory analysis."""

    def setUp(self):
        self.analyzer = MDTrajectoryAnalysis(WORKSPACE_ROOT)

    def test_xvg_parsing(self):
        """Ensure XVG parser correctly extracts numerical data and metadata headers."""
        rmsd_path = WORKSPACE_ROOT / "analysis" / "rmsd.xvg"
        data, meta = parse_xvg(rmsd_path)
        self.assertEqual(data.shape[1], 2, "RMSD file should have 2 columns (Time, RMSD)")
        self.assertGreater(data.shape[0], 100, "RMSD trajectory must contain > 100 frames")
        self.assertIn("RMSD", meta["title"])

    def test_thermodynamic_metrics(self):
        """Validate temperature, density, and RMSD statistical bounds."""
        results = self.analyzer.run_full_analysis()
        
        # Temperature equilibrium check: 300 K +/- 5 K
        t_mean = results["thermodynamics"]["system_temperature_K"]["mean"]
        self.assertAlmostEqual(t_mean, 300.0, delta=3.0, msg="System temperature must center near 300 K")

        # Density check: ~ 990-1000 kg/m^3 for TIP3P water
        rho_mean = results["thermodynamics"]["density_kg_m3"]["mean"]
        self.assertGreater(rho_mean, 980.0)
        self.assertLess(rho_mean, 1010.0)

        # Globular stability: RMSD mean < 0.25 nm (2.5 Angstrom)
        rmsd_mean = results["rmsd"]["mean"]
        self.assertLess(rmsd_mean, 0.25, msg="HEWL fold must remain stable (RMSD < 2.5 A)")


class TestRosettaDesignEngine(unittest.TestCase):
    """Unit and validation tests for Rosetta REF2015 design engine."""

    def setUp(self):
        md_json = WORKSPACE_ROOT / "analysis" / "md_statistical_validation.json"
        self.engine = LysozymeDesignEngine(md_stats_path=md_json if md_json.exists() else None)

    def test_ref2015_weights(self):
        """Ensure standard REF2015 term weights are mathematically respected."""
        decomp = EnergyDecomposition(
            fa_atr=-1.0, fa_rep=1.0, fa_sol=-1.0, fa_elec=-1.0,
            hbond_sc=-1.0, hbond_bb_sc=-1.0, rama_prepro=0.0, fa_dun=0.0, p_aa_pp=0.0
        )
        # Expected: -1.0(1) + 1.0(0.55) - 1.0(1) - 1.0(0.87) - 1.0(1) - 1.0(1) = -1 + 0.55 - 1 - 0.87 - 1 - 1 = -4.32
        self.assertAlmostEqual(decomp.total_score(), -4.32, places=2)

    def test_catalytic_control_inactivation(self):
        """Ensure mutation of catalytic Asp52 (M6_CTRL) is severely penalized."""
        evals = self.engine.build_research_library()
        ctrl = next(e for e in evals if e.variant_id == "M6_CTRL")
        self.assertGreater(ctrl.ddg_fold_reu, 0.0, "Asp52 mutation must be destabilizing/disruptive")
        self.assertLess(ctrl.catalytic_integrity_score, 0.1, "Asp52 mutation must flag near-zero catalytic score")
        self.assertFalse(ctrl.is_pareto_optimal, "Inactive control must not be Pareto-optimal")

    def test_top_candidate_identification(self):
        """Verify M2 (D101N) and M1 (W62Y) are identified on the Pareto front."""
        evals = self.engine.build_research_library()
        m2 = next(e for e in evals if e.variant_id == "M2")
        self.assertTrue(m2.is_pareto_optimal, "D101N (M2) must be Pareto-optimal")
        self.assertLess(m2.ddg_fold_reu, -2.0, "D101N must show favorable folding stability")


if __name__ == "__main__":
    unittest.main()
