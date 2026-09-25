# Diffusion Models for Intrinsically Disordered Protein (IDP) Conformational Ensembles

[![DeepBioResearch](https://img.shields.io/badge/Agent-DeepBioResearch-blue.svg)](https://github.com/rabbitego)
[![Domain](https://img.shields.io/badge/Domain-Structural%20Biology%20%7C%20IDPs-green.svg)](https://proteinensemble.org)
[![Diffusion](https://img.shields.io/badge/Diffusion-Torsion%20Torus%20T%5En-orange.svg)](https://doi.org/10.1038/s41467-024-45051-2)

An evidence-grounded computational biology research project investigating **Torsion-Angle Diffusion Probabilistic Models on the flat torus $\mathbb{T}^n = (\mathbb{S}^1)^n$** for learning and generating conformational landscapes of **Intrinsically Disordered Proteins (IDPs)**.

---

## 1. Key Research Deliverables

- **`IDP_DIFFUSION_RESEARCH_REPORT.md`**: Complete, multi-source validated systematic research report covering all 13 required scientific audit sections.
- **`IDP_Conformational_Ensembles_Diffusion_Report.pdf`**: Publication-grade PDF report with embedded 300-DPI polymer scaling and architecture benchmark figures.
- **`scripts/idp_diffusion_benchmark.py`**: Python suite implementing NeRF forward kinematics, polymer scaling ($\nu$), Ramachandran circular statistics, and Debye SAXS simulation.
- **`scripts/generate_idp_report_pdf.py`**: Automated PDF compilation script.
- **`tests/test_idp_benchmark.py`**: Automated unit and validation test suite.

---

## 2. Core Scientific Findings

1. **Physical Necessity of Torsion-Space Diffusion:**
   - Cartesian $SE(3)$ diffusion models (e.g. RFdiffusion, Chroma) suffer from artificial compaction when applied to disordered proteins.
   - Operating directly on backbone torsion angles $(\phi, \psi, \omega)$ on the periodic flat torus $\mathbb{T}^n = (\mathbb{S}^1)^n$ strictly preserves covalent bond geometry (via NeRF reconstruction) and eliminates unphysical bond stretching.
2. **Benchmark Datasets:**
   - **Protein Ensemble Database (PED)**: Provides gold-standard experimentally restrained IDP conformational ensembles.
   - **DisProt**: Annotated intrinsically disordered regions.
3. **Experimental Validation Standards:**
   - Small-Angle X-ray Scattering (SAXS) dimensionless Kratky plots.
   - NMR backbone chemical shifts ($^{13}\text{C}_\alpha, ^{13}\text{C}_\beta, ^{15}\text{N}, ^1\text{H}_\alpha$ via SPARTA+/SHIFTX2), RDCs, and PREs.
   - Bayesian Maximum Entropy (BME) reweighting.

---

## 3. Running the Pipeline & Tests

```powershell
# Navigate to separate project directory
cd idp_diffusion_research

# Run benchmark and generate publication figures
python scripts/idp_diffusion_benchmark.py

# Run unit tests
python -m unittest tests/test_idp_benchmark.py

# Generate PDF Research Report
python scripts/generate_idp_report_pdf.py
```
