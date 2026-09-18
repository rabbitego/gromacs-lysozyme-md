# Lysozyme GROMACS MD Demo Project

This repository documents the completed 10 ns lysozyme molecular dynamics study and keeps the project focused on the curated files that are useful for GitHub presentation and reproducibility.

## Project summary

- System: Lysozyme
- PDB: 1AKI
- Force field: AMBER99SB-ILDN
- Water model: TIP3P
- Temperature: 300 K
- Pressure: 1 bar
- Timestep: 0.002 ps (2 fs)
- Production MD: 10 ns
- Total production steps: 5,000,000
- Production length: 10,000 ps = 10 ns

## Completed workflow

1. PDB preparation
2. Topology generation (gmx pdb2gmx)
3. Box definition (gmx editconf)
4. Solvation (gmx solvate)
5. Ion neutralization (gmx genion)
6. Energy minimization (gmx mdrun)
7. NVT equilibration
8. NPT equilibration
9. Production MD
10. Trajectory analysis (gmx rms, gmx rmsf, gmx gyrate, gmx hbond, gmx energy)

## Verified run details

The production run completed successfully and the log shows the system reached 5,000,000 steps, corresponding to 10,000 ps or 10 ns.

Observed summary metrics from the analysis output:

- RMSD average: about 0.153 nm
- Radius of gyration: about 1.42 nm with no obvious progressive expansion or collapse
- Hydrogen bonds: average about 101.844 per frame
- Production temperature: around 300.003 K
- Production pressure: about 1.293 bar average, with large instantaneous fluctuations
- Production volume: about 390.369 nm^3
- Production density: about 992.165 kg/m^3
- RMSF: mostly around 0.04-0.08 nm, with local flexible regions

These values should be treated as a demonstration-level result rather than publication-grade evidence of long-term biological stability.

## Scientific limitations

This project is intentionally kept as a learning/demo MD study.

- NVT equilibration: 100 ps
- NPT equilibration: 100 ps
- Production: 10 ns
- This is short for many protein questions
- Pressure shows large instantaneous fluctuations in MD
- The goal is portfolio and demonstration value, not definitive biological conclusions

## Repository structure

```text
gromacs-lysozyme-md/
|-- README.md
|-- .gitignore
|-- input/
|   |-- 1AKI.pdb
|   |-- minim.mdp
|   |-- nvt.mdp
|   |-- npt.mdp
|   `-- md.mdp
|-- topology/
|   `-- topol.top
|-- analysis/
|   |-- rmsd.xvg
|   |-- rmsf.xvg
|   |-- gyrate.xvg
|   |-- hbond.xvg
|   `-- md_energy.xvg
`-- figures/
    |-- rmsd.png
    |-- rmsf.png
    |-- gyrate.png
    |-- hbond.png
    `-- md_energy.png
```

## Notes on portfolio scope

The portfolio intentionally keeps only the files needed to document the simulation workflow, analysis, and results. Large trajectory and checkpoint data are excluded from the repository, while the original simulation outputs remain untouched in the original working directory.

The redundant `npt_energy.xvg` copy is not included in the portfolio because it does not add meaningful value beyond `md_energy.xvg` and the cleaner portfolio keeps only the most useful summary energy trace.

## Summary

This is a completed 10 ns lysozyme GROMACS learning/demo project. It is useful for demonstrating a full MD workflow, file organization, and analysis, while remaining scientifically honest about the limits of a short simulation trajectory.
