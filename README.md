# Research-Grade Molecular Dynamics & Computational Enzyme Design: Hen Egg-White Lysozyme (HEWL)

[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![GROMACS](https://img.shields.io/badge/GROMACS-2023.3-orange.svg)](https://www.gromacs.org/)
[![Rosetta REF2015](https://img.shields.io/badge/Rosetta-REF2015-green.svg)](https://www.rosettacommons.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

An end-to-end computational biophysics and protein engineering investigation of Hen Egg-White Lysozyme (**HEWL**, PDB: `1AKI`, EC 3.2.1.17). This repository integrates **10 ns all-atom Molecular Dynamics (MD) equilibrium trajectories** with **Rosetta REF2015 rational enzyme design**, Pareto multi-objective optimization, and wet-lab translational validation protocols.

---

## 1. Scientific Overview & Objectives

1. **Equilibrium Dynamics & Thermodynamic Invariance:**
   - Establish baseline conformational dynamics and thermodynamic stability of HEWL in explicit TIP3P solvent under an isobaric-isothermal ($NPT$) ensemble ($T = 300\text{ K}$, $P = 1.0\text{ bar}$).
   - Quantify equilibrium convergence, autocorrelation time ($\tau_{int}$), effective sample size ($N_{eff}$), and theoretical crystallographic $B$-factors ($B_i = \frac{8\pi^2}{3} \text{RMSF}_i^2$).
2. **Subsite-Specific Active Cleft Remodeling:**
   - Map carbohydrate binding subsites ($\text{A}$ through $\text{F}$) in the substrate-binding cleft.
   - Enforce catalytic dyad inviolability (`Glu35` general acid, $\text{p}K_a \approx 6.2$; `Asp52` nucleophile, $\text{p}K_a \approx 3.7$).
   - Screen rational substitutions targeting substrate selectivity and oligosaccharide binding without perturbing fold stability ($\Delta\Delta G_{fold} \le 0$) or catalytic transition-state geometry.

---

## 2. Quantitative Biophysical Findings (Validated 10 ns Trajectory)

Statistical quantities computed using block averaging and integrated autocorrelation correction ($N_{eff}$):

| Biophysical Observable | Symbol / Metric | Mean $\pm \text{Std}$ | Standard Error ($\text{SEM}$) | 95% Confidence Interval | Stationarity Status |
|---|---|---|---|---|---|
| **Backbone C$\alpha$ RMSD** | $\text{RMSD}$ | $0.153 \pm 0.015\text{ nm}$ | $0.0042\text{ nm}$ | $[0.144, 0.161]\text{ nm}$ | Converged & Stationary |
| **Radius of Gyration ($R_g$)** | $R_g$ | $1.418 \pm 0.007\text{ nm}$ | $0.0007\text{ nm}$ | $[1.417, 1.420]\text{ nm}$ | Stable Compact Globule |
| **Shape Anisotropy** | $\kappa^2$ | $0.018 \pm 0.005$ | $0.0006$ | $[0.017, 0.019]$ | Prolate Spheroid |
| **Intramolecular H-Bonds** | $N_{HB}$ | $101.84 \pm 4.45$ | $0.44\text{ count}$ | $[100.97, 102.71]$ | Intact Secondary Structure |
| **Thermodynamic Temp** | $T$ | $300.02 \pm 1.68\text{ K}$ | $0.17\text{ K}$ | $[299.69, 300.35]\text{ K}$ | Gaussian Equilibrium ($T=300\text{ K}$) |
| **Ensemble Pressure** | $P$ | $1.29 \pm 153.2\text{ bar}$ | $15.3\text{ bar}$ | $[-28.7, 31.3]\text{ bar}$ | Normal MD Virial Variance |
| **Solvent Density** | $\rho$ | $992.35 \pm 4.48\text{ kg/m}^3$ | $0.45\text{ kg/m}^3$ | $[991.47, 993.23]\text{ kg/m}^3$ | Correct for TIP3P at 300 K |
| **Total Energy** | $E_{tot}$ | $-405520 \pm 481\text{ kJ/mol}$ | $48.1\text{ kJ/mol}$ | Conservative | Negligible drift ($\Delta E / \Delta t \approx 0$) |

### Catalytic Core Rigidity vs Loop Flexibility
- **Catalytic Acid (`Glu35`):** $\text{RMSF} = 0.0435\text{ nm}$ ($B = 4.96\text{ \AA}^2$) $\rightarrow$ Highly rigidified catalytic microenvironment.
- **Catalytic Nucleophile (`Asp52`):** $\text{RMSF} = 0.0573\text{ nm}$ ($B = 8.63\text{ \AA}^2$) $\rightarrow$ Well-constrained solvent-exposed active loop.
- **Subsite B Clamp (`Trp62`):** $\text{RMSF} = 0.0460\text{ nm}$ ($B = 5.56\text{ \AA}^2$) $\rightarrow$ Stable aromatic stacking platform.
- **Subsite D Distortion (`Trp108`):** $\text{RMSF} = 0.0422\text{ nm}$ ($B = 4.68\text{ \AA}^2$) $\rightarrow$ Rigidified packing floor against `Glu35`.

---

## 3. Rosetta REF2015 Mutational Design & Pareto Optimization

Using the full **REF2015** scoring potential ($fa\_atr, fa\_rep, fa\_sol, fa\_elec, hbond\_sc, hbond\_bb\_sc, rama\_prepro, fa\_dun, p\_aa\_pp$), candidate mutations were evaluated across two orthogonal objectives: **folding stability ($\Delta\Delta G_{fold}$)** and **substrate binding affinity ($\Delta\Delta G_{bind}$)**.

```mermaid
quadrantChart
    title Rosetta Enzyme Design Mutational Landscape
    x-axis Destabilizing (ddG > 0) --> Stabilizing (ddG < 0)
    y-axis Weaker Binding (ddG > 0) --> Tighter Binding (ddG < 0)
    quadrant-1 Unfavorable / Disruptive
    quadrant-2 Selective Destabilization
    quadrant-3 Non-binding Stabilizer
    quadrant-4 Optimal Design Space (Pareto Front)
    "M2: D101N": [0.85, 0.88]
    "M1: W62Y": [0.75, 0.72]
    "M5: R45K": [0.65, 0.60]
    "M4: N59S": [0.55, 0.52]
    "M3: W108F": [0.35, 0.38]
    "M6_CTRL (D52E)": [0.10, 0.12]
```

### Prioritized Design Candidate Table

| ID | Mutation | Target Subsite | $\Delta\Delta G_{fold}$ (REU) | $\Delta\Delta G_{fold}$ (kcal/mol) | $\Delta\Delta G_{bind}$ (REU) | Catalytic Score | Pareto Status | Primary Mechanism |
|---|---|---|---|---|---|---|---|---|
| **M2** | `Asp101Asn` | Subsite A | **-3.06** | **-1.99** | **-1.95** | **1.00** | **Optimal (Rank 1)** | Eliminates electrostatic repulsion with modified/deacetylated polymers while preserving H-bonding. |
| **M1** | `Trp62Tyr` | Subsite B | **-2.28** | **-1.48** | **-1.35** | **0.98** | **Optimal (Rank 2)** | Tunes aromatic clamp stacking footprint while retaining phenolic hydroxyl H-bond. |
| **M5** | `Arg45Lys` | Subsite E | **-1.44** | **-0.93** | **-0.85** | **0.99** | **Optimal (Rank 3)** | Isoelectric steering conservation with reduced steric hindrance at product release channel. |
| **M4** | `Asn59Ser` | Subsite B/C | **-0.90** | **-0.58** | **-0.55** | **0.99** | Non-dominated | Cleft rim widening for branched or bulky oligosaccharides. |
| **M7** | `Ala107Gly` | Subsite C | **-0.34** | **-0.22** | **-0.40** | **0.96** | Non-dominated | Subsite floor conformational flexibility. |
| **M8** | `Ile98Val` | Subsite C | **-0.18** | **-0.12** | **-0.25** | **0.99** | Non-dominated | Micro-cavity packing adjustment. |
| **M3** | `Trp108Phe` | Subsite D | **+1.31** | **+0.85** | **+0.80** | **0.72** | Mechanistic Probe | Relieves subsite D steric strain; potential trade-off on transition-state distortion. |
| **M6** | `Asp52Glu` | Subsite D | **+3.47** | **+2.26** | **+2.10** | **0.05** | Negative Control | Perturbs catalytic nucleophile geometry ($\approx 100\%$ inactivation). |

---

## 4. Repository Structure & Artifacts

```text
.
|-- README.md                             # Comprehensive research documentation
|-- RESEARCH_SUMMARY.md                   # Full research summary & scientific report
|-- requirements.txt                      # Verified Python dependencies
|-- scripts/
|   `-- analyze_md_trajectory.py          # Research-grade GROMACS XVG statistical analysis suite
|-- tests/
|   `-- test_pipeline.py                  # Automated unit and integration test suite
|-- input/
|   |-- 1AKI.pdb                          # High-resolution HEWL crystal structure
|   |-- minim.mdp                         # Steepest descent energy minimization
|   |-- nvt.mdp                           # NVT equilibration (V-rescale thermostat, 300 K)
|   |-- npt.mdp                           # NPT equilibration (Parrinello-Rahman barostat, 1 bar)
|   `-- md.mdp                            # 10 ns production MD protocol
|-- topology/
|   `-- topol.top                         # AMBER99SB-ILDN topology with TIP3P water
|-- analysis/
|   |-- md_statistical_validation.json    # Machine-readable statistical metrics & convergence data
|   |-- md_summary_metrics.csv            # Formatted biophysical summary table
|   |-- rmsd.xvg                          # C-alpha backbone trajectory RMSD
|   |-- rmsf.xvg                          # Residue-resolved root-mean-square fluctuation
|   |-- gyrate.xvg                        # Radius of gyration and directional tensors
|   |-- hbond.xvg                         # Intramolecular hydrogen bond time series
|   `-- md_energy.xvg                     # Thermodynamic energy, T, P, and density traces
|-- figures/
|   |-- md_comprehensive_analysis.png     # 6-panel composite publication figure (300 DPI)
|   `-- rmsf_bfactor_landscape.png        # Residue dynamics & theoretical B-factor map
`-- rosetta_learning/
    |-- lysozyme_design_memo.md           # Formal enzyme engineering technical memo
    |-- rosetta_deep_dive.md              # Deep-dive theory on Rosetta energy functions
    |-- analysis/
    |   |-- mutant_energy_evaluation.csv  # REF2015 energy component breakdown
    |   `-- mutant_pareto_ranking.json    # Pareto front optimization records
    |-- figures/
    |   |-- rosetta_pareto_landscape.png  # Multi-objective Pareto frontier visualization
    |   |-- rosetta_energy_decomposition.png # Detailed per-term energy contributions
    |   `-- rosetta_energy_terms.png      # REF2015 scoring function weight distribution
    |-- input/
    |   |-- enzyme_design.xml             # RosettaScripts XML protocol
    |   |-- flags                         # Rosetta command-line flags
    |   `-- lysozyme_design.resfile       # Residue-level packing & design instructions
    `-- src/
        |-- rosetta_engine.py             # Research-grade Rosetta & Pareto design engine
        |-- rosetta_learning.py           # Core candidate data models & ranking routines
        |-- lysozyme_design_brief.py      # Automated brief generator
        |-- visualize_rosetta.py          # Figure generation routines
        `-- design_exercise.py            # Educational design framework
```

---

## 5. Reproduction & Execution

### 1. Environment Setup
```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Run Trajectory Analysis & Statistical Validation
```powershell
python scripts/analyze_md_trajectory.py
```

### 3. Run Rosetta Design Engine & Pareto Optimization
```powershell
python rosetta_learning/src/rosetta_engine.py
```

### 4. Run Test Suite
```powershell
python -m unittest tests/test_pipeline.py
```

---

## 6. Wet-Lab Experimental Validation Protocol

To translate these computational designs into physical validation:

1. **Recombinant Overexpression:**
   - Vector: `pET-28a(+)` with $N$-terminal $\text{His}_6$-tag and TEV protease cleavage site.
   - Host: *E. coli* BL21(DE3) or *Pichia pastoris* X-33 (for correct disulfide bond formation across 4 native SS-bonds: Cys6-Cys127, Cys30-Cys115, Cys64-Cys80, Cys76-Cys94).
2. **Thermal Stability Characterization:**
   - **nanoDSF (Differential Scanning Fluorimetry):** Measure intrinsic tryptophan fluorescence emission ratio ($F_{350}/F_{330}$) across $20^\circ\text{C} \rightarrow 95^\circ\text{C}$ ramp ($1^\circ\text{C/min}$). Determine $T_m$ and $T_{onset}$. Acceptance threshold: $\Delta T_m \ge -2.0^\circ\text{C}$ vs wild-type.
3. **Enzyme Kinetics & Subsite Specificity Assays:**
   - **Bacterial Cell Wall Clearance:** Turbidimetric clearance assay using lyophilized *Micrococcus lysodeikticus* cells (OD$_{450}$ monitoring in 66 mM potassium phosphate buffer, pH 6.24 at $25^\circ\text{C}$).
   - **Fluorogenic Oligosaccharide Assay:** 4-Methylumbelliferyl-$\beta$-D-glycoside ($4\text{-MUG}_n$) substrates to quantify subsite-specific catalytic parameters ($k_{cat}, K_M, k_{cat}/K_M$).

