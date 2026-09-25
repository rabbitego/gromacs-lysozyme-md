#!/usr/bin/env python3
"""
Unit and Validation Tests for IDP Diffusion Framework & Biometrics
==================================================================
"""

import sys
import unittest
from pathlib import Path
import numpy as np

WORKSPACE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(WORKSPACE / "scripts"))

from idp_diffusion_benchmark import (
    torsion_to_backbone_nerf,
    compute_radius_of_gyration,
    compute_end_to_end_distance,
    simulate_debye_saxs
)


class TestIDPBenchmark(unittest.TestCase):
    """Tests for forward kinematics, polymer biometrics, and SAXS Debye scattering."""

    def test_nerf_forward_kinematics(self):
        """Test NeRF reconstruction generates valid backbone bond lengths."""
        # 10 residue poly-alanine alpha-helix (phi=-60, psi=-45)
        phi = np.full(10, -60.0)
        psi = np.full(10, -45.0)
        coords = torsion_to_backbone_nerf(phi, psi)
        
        # 10 residues * 3 atoms (N, CA, C) = 30 atoms
        self.assertEqual(coords.shape, (30, 3))
        
        # Check N-CA bond length (~1.46 A)
        n_ca_dist = np.linalg.norm(coords[1] - coords[0])
        self.assertAlmostEqual(n_ca_dist, 1.46, places=2)
        
        # Check CA-C bond length (~1.52 A)
        ca_c_dist = np.linalg.norm(coords[2] - coords[1])
        self.assertAlmostEqual(ca_c_dist, 1.52, places=2)

    def test_radius_of_gyration_and_end_to_end(self):
        """Test Rg and Ree for extended vs helical chains."""
        # Extended beta strand (phi=-120, psi=+130)
        phi_ext = np.full(20, -120.0)
        psi_ext = np.full(20, 130.0)
        coords_ext = torsion_to_backbone_nerf(phi_ext, psi_ext)
        ca_ext = coords_ext[1::3] # Take CA atoms
        
        rg_ext = compute_radius_of_gyration(ca_ext)
        ree_ext = compute_end_to_end_distance(ca_ext)
        
        # Alpha helix
        phi_hel = np.full(20, -60.0)
        psi_hel = np.full(20, -45.0)
        coords_hel = torsion_to_backbone_nerf(phi_hel, psi_hel)
        ca_hel = coords_hel[1::3]
        
        rg_hel = compute_radius_of_gyration(ca_hel)
        ree_hel = compute_end_to_end_distance(ca_hel)
        
        # Extended chain must have significantly larger Rg and Ree than compact helix
        self.assertGreater(rg_ext, rg_hel)
        self.assertGreater(ree_ext, ree_hel)

    def test_debye_saxs_scattering(self):
        """Test Debye SAXS intensity profile properties."""
        phi = np.full(15, -65.0)
        psi = np.full(15, 145.0) # PPII
        coords = torsion_to_backbone_nerf(phi, psi)
        ca = coords[1::3]
        
        q_vals = np.linspace(0.0, 0.5, 50)
        iq = simulate_debye_saxs(ca, q_vals)
        
        # I(0) normalized to 1.0
        self.assertAlmostEqual(iq[0], 1.0, places=4)
        # Intensity must decay monotonically at low q (Guinier region)
        self.assertGreater(iq[0], iq[10])


if __name__ == "__main__":
    unittest.main()
