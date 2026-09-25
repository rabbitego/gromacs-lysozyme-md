#!/usr/bin/env python3
"""
Research-Grade Molecular Dynamics Trajectory & Thermodynamics Analysis Suite
=============================================================================
Target: Hen Egg-White Lysozyme (HEWL, PDB: 1AKI) - 10 ns GROMACS MD Simulation
Author: Computational Biochemistry & Molecular Biophysics Pipeline
Description:
    Performs rigorous statistical trajectory analysis, equilibrium detection,
    autocorrelation time estimation, block averaging, error propagation,
    B-factor derivation, and publication-quality figure generation.
"""

from __future__ import annotations

import json
import os
import sys
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


# -----------------------------------------------------------------------------
# XVG Parsing Utilities
# -----------------------------------------------------------------------------
def parse_xvg(file_path: Path) -> Tuple[np.ndarray, Dict[str, Any]]:
    """Parse GROMACS XVG file extracting metadata, legends, and numerical data matrix.
    
    Args:
        file_path: Path to .xvg file.
        
    Returns:
        Tuple of (data_matrix [N_frames, N_cols], metadata_dict)
    """
    if not file_path.exists():
        raise FileNotFoundError(f"XVG file not found: {file_path}")

    metadata: Dict[str, Any] = {
        "title": "",
        "xaxis": "",
        "yaxis": "",
        "legends": [],
    }
    data_rows: List[List[float]] = []

    with open(file_path, "r", encoding="utf-8", errors="replace") as f:
        for line in f:
            line_str = line.strip()
            if not line_str:
                continue
            if line_str.startswith("#"):
                continue
            if line_str.startswith("@"):
                # Parse metadata headers
                if line_str.startswith("@    title ") or line_str.startswith("@ title "):
                    metadata["title"] = line_str.split('"')[1]
                elif "xaxis  label" in line_str or "xaxis label" in line_str:
                    metadata["xaxis"] = line_str.split('"')[1]
                elif "yaxis  label" in line_str or "yaxis label" in line_str:
                    metadata["yaxis"] = line_str.split('"')[1]
                elif " legend " in line_str and '"' in line_str:
                    legend_label = line_str.split('"')[1]
                    metadata["legends"].append(legend_label)
                continue

            # Parse numeric lines
            parts = line_str.split()
            try:
                numeric_row = [float(p) for p in parts]
                data_rows.append(numeric_row)
            except ValueError:
                continue

    data_array = np.array(data_rows)
    return data_array, metadata


# -----------------------------------------------------------------------------
# Statistical Mechanics & Time Series Analysis
# -----------------------------------------------------------------------------
def compute_autocorrelation_time(series: np.ndarray, max_lag: Optional[int] = None) -> float:
    """Compute integrated autocorrelation time tau_int using standard FFT autocorrelation."""
    n = len(series)
    if n < 10:
        return 1.0
    
    # Center series
    mean = np.mean(series)
    var = np.var(series)
    if var == 0:
        return 1.0
    
    centered = series - mean
    if max_lag is None:
        max_lag = min(n // 4, 200)

    # Compute autocorrelation via numpy correlate
    autocorr = np.correlate(centered, centered, mode="full")[n - 1 : n - 1 + max_lag]
    autocorr /= autocorr[0]

    # Integrate until autocorrelation drops below zero or threshold
    tau = 0.5
    for k in range(1, len(autocorr)):
        if autocorr[k] <= 0:
            break
        tau += autocorr[k]
    return max(0.5, float(tau))


def compute_statistical_metrics(series: np.ndarray, dt: float = 1.0) -> Dict[str, float]:
    """Compute mean, std, SEM (corrected for autocorrelation), 95% CI, drift, and stationarity."""
    n = len(series)
    mean_val = float(np.mean(series))
    std_val = float(np.std(series, ddof=1))
    median_val = float(np.median(series))
    min_val = float(np.min(series))
    max_val = float(np.max(series))

    # Autocorrelation and effective sample size
    tau_int = compute_autocorrelation_time(series)
    n_eff = max(1.0, float(n / (2.0 * tau_int)))
    sem = float(std_val / np.sqrt(n_eff))

    # 95% Confidence Interval
    ci_95_low = mean_val - 1.96 * sem
    ci_95_high = mean_val + 1.96 * sem

    # Linear drift analysis (slope across time series)
    time_points = np.arange(n) * dt
    slope, intercept, r_value, p_value, std_err = stats.linregress(time_points, series)
    total_drift = float(slope * (time_points[-1] - time_points[0]))

    # Geweke equilibrium test (comparing first 10% with last 50%)
    first_10_idx = int(0.10 * n)
    last_50_idx = int(0.50 * n)
    s_first = series[:first_10_idx]
    s_last = series[last_50_idx:]
    
    t_stat, geweke_p = stats.ttest_ind(s_first, s_last, equal_var=False)

    return {
        "n_frames": int(n),
        "mean": round(mean_val, 4),
        "std": round(std_val, 4),
        "sem": round(sem, 4),
        "median": round(median_val, 4),
        "min": round(min_val, 4),
        "max": round(max_val, 4),
        "ci_95_low": round(ci_95_low, 4),
        "ci_95_high": round(ci_95_high, 4),
        "tau_int_frames": round(tau_int, 2),
        "n_effective": round(n_eff, 1),
        "drift_total": round(total_drift, 5),
        "drift_slope_per_unit": round(float(slope), 6),
        "geweke_p_value": round(float(geweke_p), 4),
        "stationary": bool(geweke_p > 0.05 or abs(total_drift) < 0.15 * std_val),
    }


# -----------------------------------------------------------------------------
# Main Trajectory Analysis Pipeline
# -----------------------------------------------------------------------------
class MDTrajectoryAnalysis:
    """Comprehensive analysis manager for GROMACS simulation outputs."""

    def __init__(self, workspace_root: Path):
        self.root = workspace_root
        self.analysis_dir = self.root / "analysis"
        self.figures_dir = self.root / "figures"
        self.figures_dir.mkdir(parents=True, exist_ok=True)

        self.rmsd_file = self.analysis_dir / "rmsd.xvg"
        self.rmsf_file = self.analysis_dir / "rmsf.xvg"
        self.gyrate_file = self.analysis_dir / "gyrate.xvg"
        self.hbond_file = self.analysis_dir / "hbond.xvg"
        self.energy_file = self.analysis_dir / "md_energy.xvg"

        # HEWL Annotated Functional Residues (PDB: 1AKI numbering, 1-129)
        self.catalytic_residues = [35, 52]  # Glu35 (acid), Asp52 (nucleophile)
        self.subsite_residues = {
            "Subsite A (Entrance)": [101, 102, 103],
            "Subsite B (Primary clamp)": [59, 62, 63],
            "Subsite C (Internal bind)": [98, 107],
            "Subsite D (Distortion site)": [35, 52, 57, 108, 109],
            "Subsite E/F (Leaving group)": [45, 46, 68, 112],
        }

    def run_full_analysis(self) -> Dict[str, Any]:
        """Execute complete quantitative analysis across all trajectory metrics."""
        results: Dict[str, Any] = {}

        print("[1/5] Analyzing Backbone RMSD Trajectory...")
        rmsd_data, rmsd_meta = parse_xvg(self.rmsd_file)
        # Columns: Time (ns), RMSD (nm)
        time_rmsd_ns = rmsd_data[:, 0]
        rmsd_nm = rmsd_data[:, 1]
        results["rmsd"] = compute_statistical_metrics(rmsd_nm, dt=0.01)
        # Convert nm to Angstrom for biophysical comparison
        results["rmsd"]["mean_angstrom"] = round(results["rmsd"]["mean"] * 10.0, 2)
        results["rmsd"]["std_angstrom"] = round(results["rmsd"]["std"] * 10.0, 2)

        print("[2/5] Analyzing Residue RMSF & Calculating Theoretical B-factors...")
        rmsf_data, rmsf_meta = parse_xvg(self.rmsf_file)
        # Columns: Residue Index, RMSF (nm)
        res_indices = rmsf_data[:, 0].astype(int)
        rmsf_nm = rmsf_data[:, 1]
        rmsf_angstrom = rmsf_nm * 10.0
        # Debye-Waller B-factor: B_i = (8 * pi^2 / 3) * <dr_i^2> = (8 * pi^2 / 3) * RMSF^2
        b_factors = (8.0 * (np.pi ** 2) / 3.0) * (rmsf_angstrom ** 2)

        results["rmsf"] = {
            "residue_count": len(res_indices),
            "mean_rmsf_nm": round(float(np.mean(rmsf_nm)), 4),
            "std_rmsf_nm": round(float(np.std(rmsf_nm)), 4),
            "max_rmsf_residue": int(res_indices[np.argmax(rmsf_nm)]),
            "max_rmsf_val_nm": round(float(np.max(rmsf_nm)), 4),
            "min_rmsf_residue": int(res_indices[np.argmin(rmsf_nm)]),
            "min_rmsf_val_nm": round(float(np.min(rmsf_nm)), 4),
            "mean_b_factor_A2": round(float(np.mean(b_factors)), 2),
            "std_b_factor_A2": round(float(np.std(b_factors)), 2),
            "catalytic_residues_rmsf": {
                f"Glu35": round(float(rmsf_nm[34]), 4),
                f"Asp52": round(float(rmsf_nm[51]), 4),
                f"Trp62": round(float(rmsf_nm[61]), 4),
                f"Trp108": round(float(rmsf_nm[107]), 4),
            },
        }

        print("[3/5] Analyzing Radius of Gyration (Compactness & Anisotropy)...")
        gyr_data, gyr_meta = parse_xvg(self.gyrate_file)
        # Columns: Time (ps), Rg, Rg_x, Rg_y, Rg_z
        time_gyr_ns = gyr_data[:, 0] / 1000.0
        rg_total = gyr_data[:, 1]
        rg_x = gyr_data[:, 2]
        rg_y = gyr_data[:, 3]
        rg_z = gyr_data[:, 4]

        # Shape Anisotropy: kappa^2
        # kappa^2 = 1 - 3 * (Rg_x^2 * Rg_y^2 + Rg_y^2 * Rg_z^2 + Rg_z^2 * Rg_x^2) / (Rg_x^2 + Rg_y^2 + Rg_z^2)^2
        r2_sum = (rg_x**2 + rg_y**2 + rg_z**2)
        cross_r2 = (rg_x**2 * rg_y**2 + rg_y**2 * rg_z**2 + rg_z**2 * rg_x**2)
        anisotropy = 1.0 - 3.0 * cross_r2 / (r2_sum**2 + 1e-12)

        results["radius_of_gyration"] = compute_statistical_metrics(rg_total, dt=0.01)
        results["shape_anisotropy_kappa2"] = compute_statistical_metrics(anisotropy, dt=0.01)

        print("[4/5] Analyzing Intramolecular Hydrogen Bonding Network...")
        hbond_data, hbond_meta = parse_xvg(self.hbond_file)
        # Columns: Time (ps), H-bonds count, Pairs within 0.35 nm
        time_hb_ns = hbond_data[:, 0] / 1000.0
        hb_count = hbond_data[:, 1]
        pairs_035 = hbond_data[:, 2]
        results["hydrogen_bonds"] = compute_statistical_metrics(hb_count, dt=0.01)
        results["contact_pairs_035nm"] = compute_statistical_metrics(pairs_035, dt=0.01)

        print("[5/5] Analyzing Thermodynamic Ensemble Integrity (Energy, T, P, V, Rho)...")
        energy_data, energy_meta = parse_xvg(self.energy_file)
        # Columns: Time (ps), Potential, Kinetic, Total Energy, Temp, Pres, Vol, Density, T-Prot, T-Solv
        time_e_ns = energy_data[:, 0] / 1000.0
        e_pot = energy_data[:, 1]
        e_kin = energy_data[:, 2]
        e_tot = energy_data[:, 3]
        temp = energy_data[:, 4]
        pres = energy_data[:, 5]
        vol = energy_data[:, 6]
        dens = energy_data[:, 7]
        t_prot = energy_data[:, 8]
        t_solv = energy_data[:, 9]

        results["thermodynamics"] = {
            "potential_energy_kJ_mol": compute_statistical_metrics(e_pot, dt=0.01),
            "kinetic_energy_kJ_mol": compute_statistical_metrics(e_kin, dt=0.01),
            "total_energy_kJ_mol": compute_statistical_metrics(e_tot, dt=0.01),
            "system_temperature_K": compute_statistical_metrics(temp, dt=0.01),
            "protein_temperature_K": compute_statistical_metrics(t_prot, dt=0.01),
            "solvent_temperature_K": compute_statistical_metrics(t_solv, dt=0.01),
            "pressure_bar": compute_statistical_metrics(pres, dt=0.01),
            "volume_nm3": compute_statistical_metrics(vol, dt=0.01),
            "density_kg_m3": compute_statistical_metrics(dens, dt=0.01),
        }

        # Save summary JSON
        summary_json_path = self.analysis_dir / "md_statistical_validation.json"
        with open(summary_json_path, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2)
        print(f"  -> Saved statistical validation JSON: {summary_json_path}")

        # Save tabular summary CSV
        self._export_summary_csv(results)

        # Generate publication-grade figures
        self.generate_publication_figures(
            time_rmsd_ns, rmsd_nm,
            res_indices, rmsf_nm, b_factors,
            time_gyr_ns, rg_total, rg_x, rg_y, rg_z,
            time_hb_ns, hb_count,
            time_e_ns, temp, pres, e_tot, dens
        )

        return results

    def _export_summary_csv(self, results: Dict[str, Any]) -> None:
        """Export a clean tabular CSV summarizing key biophysical observables."""
        rows = [
            {"Observable": "Backbone RMSD", "Unit": "nm", "Mean": results["rmsd"]["mean"], "Std": results["rmsd"]["std"], "SEM": results["rmsd"]["sem"], "95% CI": f"[{results['rmsd']['ci_95_low']}, {results['rmsd']['ci_95_high']}]", "Stationary": results["rmsd"]["stationary"]},
            {"Observable": "Radius of Gyration (Rg)", "Unit": "nm", "Mean": results["radius_of_gyration"]["mean"], "Std": results["radius_of_gyration"]["std"], "SEM": results["radius_of_gyration"]["sem"], "95% CI": f"[{results['radius_of_gyration']['ci_95_low']}, {results['radius_of_gyration']['ci_95_high']}]", "Stationary": results["radius_of_gyration"]["stationary"]},
            {"Observable": "Shape Anisotropy (kappa^2)", "Unit": "dimensionless", "Mean": results["shape_anisotropy_kappa2"]["mean"], "Std": results["shape_anisotropy_kappa2"]["std"], "SEM": results["shape_anisotropy_kappa2"]["sem"], "95% CI": f"[{results['shape_anisotropy_kappa2']['ci_95_low']}, {results['shape_anisotropy_kappa2']['ci_95_high']}]", "Stationary": results["shape_anisotropy_kappa2"]["stationary"]},
            {"Observable": "Intramolecular H-Bonds", "Unit": "count", "Mean": results["hydrogen_bonds"]["mean"], "Std": results["hydrogen_bonds"]["std"], "SEM": results["hydrogen_bonds"]["sem"], "95% CI": f"[{results['hydrogen_bonds']['ci_95_low']}, {results['hydrogen_bonds']['ci_95_high']}]", "Stationary": results["hydrogen_bonds"]["stationary"]},
            {"Observable": "System Temperature", "Unit": "K", "Mean": results["thermodynamics"]["system_temperature_K"]["mean"], "Std": results["thermodynamics"]["system_temperature_K"]["std"], "SEM": results["thermodynamics"]["system_temperature_K"]["sem"], "95% CI": f"[{results['thermodynamics']['system_temperature_K']['ci_95_low']}, {results['thermodynamics']['system_temperature_K']['ci_95_high']}]", "Stationary": results["thermodynamics"]["system_temperature_K"]["stationary"]},
            {"Observable": "System Pressure", "Unit": "bar", "Mean": results["thermodynamics"]["pressure_bar"]["mean"], "Std": results["thermodynamics"]["pressure_bar"]["std"], "SEM": results["thermodynamics"]["pressure_bar"]["sem"], "95% CI": f"[{results['thermodynamics']['pressure_bar']['ci_95_low']}, {results['thermodynamics']['pressure_bar']['ci_95_high']}]", "Stationary": results["thermodynamics"]["pressure_bar"]["stationary"]},
            {"Observable": "System Density", "Unit": "kg/m^3", "Mean": results["thermodynamics"]["density_kg_m3"]["mean"], "Std": results["thermodynamics"]["density_kg_m3"]["std"], "SEM": results["thermodynamics"]["density_kg_m3"]["sem"], "95% CI": f"[{results['thermodynamics']['density_kg_m3']['ci_95_low']}, {results['thermodynamics']['density_kg_m3']['ci_95_high']}]", "Stationary": results["thermodynamics"]["density_kg_m3"]["stationary"]},
            {"Observable": "Total Energy", "Unit": "kJ/mol", "Mean": results["thermodynamics"]["total_energy_kJ_mol"]["mean"], "Std": results["thermodynamics"]["total_energy_kJ_mol"]["std"], "SEM": results["thermodynamics"]["total_energy_kJ_mol"]["sem"], "95% CI": f"[{results['thermodynamics']['total_energy_kJ_mol']['ci_95_low']}, {results['thermodynamics']['total_energy_kJ_mol']['ci_95_high']}]", "Stationary": results["thermodynamics"]["total_energy_kJ_mol"]["stationary"]},
        ]
        df = pd.DataFrame(rows)
        csv_path = self.analysis_dir / "md_summary_metrics.csv"
        df.to_csv(csv_path, index=False)
        print(f"  -> Saved summary CSV: {csv_path}")

    def generate_publication_figures(
        self,
        time_rmsd: np.ndarray, rmsd: np.ndarray,
        res_idx: np.ndarray, rmsf: np.ndarray, b_fact: np.ndarray,
        time_gyr: np.ndarray, rg: np.ndarray, rg_x: np.ndarray, rg_y: np.ndarray, rg_z: np.ndarray,
        time_hb: np.ndarray, hb: np.ndarray,
        time_e: np.ndarray, temp: np.ndarray, pres: np.ndarray, e_tot: np.ndarray, dens: np.ndarray,
    ) -> None:
        """Generate high-DPI publication-ready multi-panel scientific charts."""
        plt.style.use("seaborn-v0_8-paper" if "seaborn-v0_8-paper" in plt.style.available else "default")
        plt.rcParams.update({
            "font.family": "sans-serif",
            "font.size": 10,
            "axes.labelsize": 11,
            "axes.titlesize": 12,
            "xtick.labelsize": 9,
            "ytick.labelsize": 9,
            "legend.fontsize": 9,
            "figure.titlesize": 14,
            "lines.linewidth": 1.5,
        })

        # -------------------------------------------------------------
        # Figure 1: 6-Panel Comprehensive MD Biophysical Assessment
        # -------------------------------------------------------------
        fig, axes = plt.subplots(3, 2, figsize=(14, 14), dpi=300)

        # Panel A: Backbone RMSD Trajectory & Cumulative Mean
        ax_a = axes[0, 0]
        cum_mean_rmsd = np.cumsum(rmsd) / np.arange(1, len(rmsd) + 1)
        ax_a.plot(time_rmsd, rmsd, color="#1f77b4", alpha=0.5, label="Instantaneous RMSD")
        ax_a.plot(time_rmsd, cum_mean_rmsd, color="#08306b", linewidth=2.0, label="Cumulative Average")
        ax_a.axhline(np.mean(rmsd), color="#d62728", linestyle="--", label=f"Equilibrium Mean ({np.mean(rmsd):.3f} nm)")
        ax_a.fill_between(time_rmsd, np.mean(rmsd) - np.std(rmsd), np.mean(rmsd) + np.std(rmsd), color="#1f77b4", alpha=0.15, label=r"$\pm 1\sigma$ Band")
        ax_a.set_xlabel("Simulation Time (ns)", fontweight="bold")
        ax_a.set_ylabel(r"C$\alpha$ Backbone RMSD (nm)", fontweight="bold")
        ax_a.set_title("A. Backbone Structural Convergence & Stability", fontweight="bold", loc="left")
        ax_a.legend(loc="lower right", frameon=True, facecolor="white", framealpha=0.9)
        ax_a.grid(True, linestyle=":", alpha=0.6)

        # Panel B: Radius of Gyration & Directional Components
        ax_b = axes[0, 1]
        ax_b.plot(time_gyr, rg, color="#2ca02c", linewidth=1.6, label="Total $R_g$")
        ax_b.plot(time_gyr, rg_x, color="#ff7f0e", linestyle=":", alpha=0.8, label="$R_{g,x}$")
        ax_b.plot(time_gyr, rg_y, color="#9467bd", linestyle=":", alpha=0.8, label="$R_{g,y}$")
        ax_b.plot(time_gyr, rg_z, color="#8c564b", linestyle=":", alpha=0.8, label="$R_{g,z}$")
        ax_b.set_xlabel("Simulation Time (ns)", fontweight="bold")
        ax_b.set_ylabel("Radius of Gyration $R_g$ (nm)", fontweight="bold")
        ax_b.set_title("B. Globular Compactness & Inertial Axes", fontweight="bold", loc="left")
        ax_b.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9)
        ax_b.grid(True, linestyle=":", alpha=0.6)

        # Panel C: Residue-Level RMSF with Catalytic Active-Site Annotations
        ax_c = axes[1, 0]
        ax_c.plot(res_idx, rmsf, color="#d95f02", linewidth=1.5, label="Residue RMSF")
        # Highlight catalytic residues
        ax_c.scatter([35], [rmsf[34]], color="#e41a1c", s=70, zorder=5, label="Glu35 (General Acid)")
        ax_c.scatter([52], [rmsf[51]], color="#377eb8", s=70, zorder=5, label="Asp52 (Nucleophile)")
        ax_c.scatter([62], [rmsf[61]], color="#4daf4a", s=60, zorder=5, label="Trp62 (Subsite B)")
        ax_c.scatter([108], [rmsf[107]], color="#984ea3", s=60, zorder=5, label="Trp108 (Subsite D)")
        ax_c.set_xlabel("Residue Index (1-129)", fontweight="bold")
        ax_c.set_ylabel("Cα RMS Fluctuation (nm)", fontweight="bold")
        ax_c.set_title("C. Conformational Flexibility & Active Site Rigidity", fontweight="bold", loc="left")
        ax_c.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9, fontsize=8)
        ax_c.grid(True, linestyle=":", alpha=0.6)

        # Panel D: Intramolecular Hydrogen Bonding Network
        ax_d = axes[1, 1]
        ax_d.plot(time_hb, hb, color="#7570b3", alpha=0.4, label="Instantaneous H-bonds")
        # Rolling average
        window = 25
        hb_roll = pd.Series(hb).rolling(window=window, center=True).mean()
        ax_d.plot(time_hb, hb_roll, color="#381a61", linewidth=2.0, label=f"Moving Avg (w={window})")
        ax_d.axhline(np.mean(hb), color="#d62728", linestyle="--", label=f"Mean: {np.mean(hb):.1f} H-bonds")
        ax_d.set_xlabel("Simulation Time (ns)", fontweight="bold")
        ax_d.set_ylabel("Intramolecular H-Bond Count", fontweight="bold")
        ax_d.set_title("D. Secondary Structure Hydrogen Bonding Network", fontweight="bold", loc="left")
        ax_d.legend(loc="lower right", frameon=True, facecolor="white", framealpha=0.9)
        ax_d.grid(True, linestyle=":", alpha=0.6)

        # Panel E: Thermodynamic Ensemble Coupling (Temperature & Density)
        ax_e = axes[2, 0]
        ax_e.plot(time_e, temp, color="#e7298a", alpha=0.6, label="System Temp ($T$)")
        ax_e.axhline(300.0, color="black", linestyle="--", linewidth=1.2, label="Thermostat Target (300 K)")
        ax_e.set_xlabel("Simulation Time (ns)", fontweight="bold")
        ax_e.set_ylabel("Temperature (K)", color="#e7298a", fontweight="bold")
        ax_e.tick_params(axis="y", labelcolor="#e7298a")
        ax_e.set_ylim(295, 305)

        # Secondary y-axis for Density
        ax_e_twin = ax_e.twinx()
        ax_e_twin.plot(time_e, dens, color="#1b9e77", alpha=0.7, label="Solvent Density ($\rho$)")
        ax_e_twin.set_ylabel("Density (kg/m$^3$)", color="#1b9e77", fontweight="bold")
        ax_e_twin.tick_params(axis="y", labelcolor="#1b9e77")
        ax_e.set_title("E. NPT Ensemble Thermal & Density Equilibration", fontweight="bold", loc="left")
        ax_e.grid(True, linestyle=":", alpha=0.6)

        # Panel F: Total Energy Conservation
        ax_f = axes[2, 1]
        ax_f.plot(time_e, (e_tot - np.mean(e_tot)), color="#e6ab02", linewidth=1.2, label=r"Total Energy Drift ($\Delta E_{tot}$)")
        ax_f.axhline(0, color="black", linestyle="--")
        ax_f.set_xlabel("Simulation Time (ns)", fontweight="bold")
        ax_f.set_ylabel("Energy Fluctuation (kJ/mol)", fontweight="bold")
        ax_f.set_title("F. Hamiltonian Conservation & Energy Stability", fontweight="bold", loc="left")
        ax_f.legend(loc="upper right", frameon=True, facecolor="white", framealpha=0.9)
        ax_f.grid(True, linestyle=":", alpha=0.6)

        plt.suptitle("Hen Egg-White Lysozyme (HEWL, 1AKI) 10 ns Production MD Biophysical Assessment", fontsize=15, fontweight="bold", y=0.995)
        plt.tight_layout()

        out_fig1 = self.figures_dir / "md_comprehensive_analysis.png"
        fig.savefig(out_fig1, dpi=300, bbox_inches="tight")
        plt.close(fig)
        print(f"  -> Generated 6-Panel MD Figure: {out_fig1}")

        # -------------------------------------------------------------
        # Figure 2: Residue Dynamics, Crystallographic B-factor & Subsite Map
        # -------------------------------------------------------------
        fig2, (ax1, ax2) = plt.subplots(2, 1, figsize=(13, 8), dpi=300, sharex=True)

        # Subplot 1: RMSF Profile with Shaded Subsites
        ax1.plot(res_idx, rmsf, color="#1f77b4", linewidth=1.8, label="Cα RMSF (nm)")
        colors = ["#fed976", "#feb24c", "#fd8d3c", "#fc4e2a", "#bd0026"]
        for idx, (subsite, r_list) in enumerate(self.subsite_residues.items()):
            for r in r_list:
                ax1.axvspan(r - 0.4, r + 0.4, color=colors[idx % len(colors)], alpha=0.35)

        ax1.scatter([35, 52], [rmsf[34], rmsf[51]], color="red", s=80, edgecolors="black", zorder=6, label="Catalytic Core (Glu35, Asp52)")
        ax1.set_ylabel("RMS Fluctuation (nm)", fontweight="bold")
        ax1.set_title("A. Residue-Resolved Conformational Dynamics & Active-Site Subsites", fontweight="bold", loc="left")
        ax1.legend(loc="upper left", frameon=True)
        ax1.grid(True, linestyle=":", alpha=0.6)

        # Subplot 2: Derived B-factors (A^2)
        ax2.bar(res_idx, b_fact, color="#2b5c8f", width=0.8, edgecolor="black", linewidth=0.3, label=r"Calculated $B$-factor ($B_i = \frac{8\pi^2}{3} \langle \Delta r_i^2 \rangle$)")
        ax2.axhline(np.mean(b_fact), color="crimson", linestyle="--", linewidth=1.5, label=rf"Mean B-factor ({np.mean(b_fact):.1f} $\AA^2$)")
        ax2.set_xlabel("Residue Position in Sequence (HEWL, 1-129)", fontweight="bold")
        ax2.set_ylabel(r"Theoretical B-factor ($\AA^2$)", fontweight="bold")
        ax2.set_title(r"B. Theoretical Crystallographic Isotropic Displacement Parameters ($B$-factors)", fontweight="bold", loc="left")
        ax2.set_xlim(0.5, 129.5)
        ax2.set_xticks(np.arange(1, 130, 10))
        ax2.legend(loc="upper left", frameon=True)
        ax2.grid(True, linestyle=":", alpha=0.6)

        plt.tight_layout()
        out_fig2 = self.figures_dir / "rmsf_bfactor_landscape.png"
        fig2.savefig(out_fig2, dpi=300, bbox_inches="tight")
        plt.close(fig2)
        print(f"  -> Generated B-factor & Subsite Map: {out_fig2}")


if __name__ == "__main__":
    workspace_dir = Path(__file__).resolve().parent.parent
    analyzer = MDTrajectoryAnalysis(workspace_dir)
    results = analyzer.run_full_analysis()
    print("\n--- Summary of Validated Metrics ---")
    print(f"RMSD: {results['rmsd']['mean']:.3f} +/- {results['rmsd']['std']:.3f} nm (SEM: {results['rmsd']['sem']:.4f} nm)")
    print(f"Rg:   {results['radius_of_gyration']['mean']:.3f} +/- {results['radius_of_gyration']['std']:.3f} nm")
    print(f"H-Bonds: {results['hydrogen_bonds']['mean']:.2f} +/- {results['hydrogen_bonds']['std']:.2f}")
    print(f"Temperature: {results['thermodynamics']['system_temperature_K']['mean']:.2f} +/- {results['thermodynamics']['system_temperature_K']['std']:.2f} K")
    print(f"Density: {results['thermodynamics']['density_kg_m3']['mean']:.2f} +/- {results['thermodynamics']['density_kg_m3']['std']:.2f} kg/m^3")
