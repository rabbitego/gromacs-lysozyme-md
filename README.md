# Lysozyme Molecular Dynamics Simulation using GROMACS

> Note: The current workspace directory was empty when this repository was initialized. No original GROMACS input, topology, or analysis files were present in the local project folder, so this repository is a clean portfolio scaffold and documentation template rather than a reconstruction of a completed run. The project should be populated with the verified outputs from the original simulation directory before public use.

## 1. Project Overview

This project documents a molecular dynamics simulation of lysozyme using GROMACS. The intended system is the lysozyme structure from PDB ID 1AKI, prepared and simulated in a solvated, neutralized, biologically realistic environment under standard biomolecular simulation conditions. The workflow includes structure preparation, equilibration, production dynamics, and trajectory analysis to characterize the stability and flexibility of the protein over a 10 ns simulation window.

## 2. Objective

The objective is to evaluate the structural behavior of lysozyme under explicit solvent conditions using force-field-based molecular dynamics. The workflow is designed to assess whether the protein remains globally compact and stable over the simulated time scale while also identifying residue-level flexibility and hydrogen-bonding behavior.

## 3. Software and Tools

- GROMACS 2023.3
- CPU-only MD simulation workflow
- AMBER99SB-ILDN force field
- TIP3P water model
- Standard GROMACS pre-processing and analysis tools
- Scientific plotting using the existing XVG outputs when available

## 4. System Information

- Protein: Lysozyme
- PDB ID: 1AKI
- Protein chain: A
- Residues: 129
- Simulation type: molecular dynamics in explicit solvent
- Temperature: 300 K
- Pressure: 1 bar
- Integration time step: 0.002 ps
- Total production simulation duration: 10 ns

## 5. Simulation Workflow

The intended simulation workflow was:

1. PDB preparation
2. Topology generation using pdb2gmx
3. Cubic box definition
4. Solvation
5. Ion addition and neutralization
6. Energy minimization
7. NVT equilibration
8. NPT equilibration
9. Production MD
10. Trajectory analysis

This sequence follows a conventional biomolecular simulation pipeline for a solvated protein system and is appropriate for a well-posed short MD study of a globular protein.

## 6. Force Field

The simulation used the AMBER99SB-ILDN force field. This force field is widely used for protein simulations because it provides a balanced description of folded protein behavior and is appropriate for a stable, residue-based biomolecular system such as lysozyme.

## 7. Water Model

The solvent model used in this setup was TIP3P water. TIP3P is a standard explicit water model for biomolecular simulations and is consistent with the chosen AMBER-based protein force field for a general-purpose protein MD study.

## 8. System Preparation

The system was prepared from the lysozyme crystal structure and converted into a GROMACS-compatible representation. Solvent molecules were added to fill a cubic box, followed by ion placement to neutralize the system. In the supplied run description, 8 chloride ions were added to neutralize the initial +8 protein charge. This is a standard practice for simulating a protein in explicit solvent when the net charge of the modeled system is positive.

## 9. Energy Minimization

Energy minimization was performed using steepest descent with the following parameters:

- Algorithm: Steepest Descent
- emtol = 1000.0
- emstep = 0.01
- nsteps = 50000
- Convergence occurred in approximately 852 steps

This step removes severe steric clashes and unrealistic geometry before the system enters equilibration.

## 10. NVT Equilibration

The NVT equilibration phase was run at 300 K for 100 ps with a 0.002 ps timestep. The thermostat was V-rescale with separate coupling groups for Protein and Water_and_ions. PME electrostatics and hydrogen-bond constraints were used, with periodic boundary conditions applied in all directions. This stage equilibrates the solvent and protein degrees of freedom to the target temperature without changing the density.

## 11. NPT Equilibration

The NPT equilibration phase was performed at 300 K and 1 bar for 100 ps. The thermostat remained V-rescale, while the barostat used Parrinello-Rahman with isotropic pressure coupling. PME electrostatics and hydrogen-bond constraints were retained. This stage equilibrates the box density and pressure to be consistent with the intended condensed-phase simulation conditions.

## 12. 10 ns Production MD

The production simulation was a 10 ns NPT MD run at 300 K and 1 bar with a 0.002 ps timestep and 5,000,000 steps. The run used V-rescale temperature coupling, Parrinello-Rahman pressure coupling, PME long-range electrostatics, and hydrogen-bond constraints. The system continued from the equilibrated state with no reinitialization of velocities. The reported wall time was approximately 7 h 17 min, corresponding to about 32.939 ns/day. The dynamic load balancing output indicated approximately 25.5% average load imbalance and about 15.4% loss of CPU time due to domain decomposition imbalance; this was a performance issue rather than a simulation failure.

## 13. Trajectory Analysis

Trajectory analysis was performed on the updated production run with standard GROMACS analysis tools. The relevant analyses include:

- RMSD
- RMSF
- Radius of gyration
- Hydrogen-bond count
- Energetics from the production .edr file

These observables provide complementary information on structural drift, flexibility, compactness, and intermolecular interaction stability.

## 14. Results

No verified experimental or analytical outputs were present in the current workspace, so no scientific claims about the observed trajectory can be made from local data in this repository. The actual simulation outputs from the original project directory were not available here, and fabricating numerical values would be misleading. This section is therefore intentionally left as a placeholder for the verified results once the original project files are restored into the repository.

## 15. Interpretation

The interpretation of a lysozyme MD trajectory depends on the actual structural metrics extracted from the production simulation. In a well-behaved short MD trajectory, one expects initial relaxation, followed by fluctuations around a stable structural ensemble for the remainder of the trajectory. A stable compact protein would typically show limited RMSD drift, modest residue-specific RMSF, consistent radius of gyration, and sustained hydrogen-bonding patterns without obvious long-term unfolding or destabilization.

## 16. GROMACS Commands Used

The intended workflow used standard GROMACS commands for structure preparation and analysis, including the following categories:

- pdb2gmx
- editconf
- solvate
- genion
- grompp
- mdrun
- gmx rms
- gmx rmsf
- gmx gyrate
- gmx hbond
- gmx energy
- gmx analyze

The exact command lines should be recorded from the original project directory and retained with the verified simulation outputs before publication.

## 17. Repository Structure

This repository is intentionally kept minimal and professional. The intended organization for a complete project is:

```text
.
├── README.md
├── .gitignore
├── input/
├── topology/
├── structures/
├── analysis/
├── results/
└── documentation/
```

The original project directory was empty in this environment, so no GROMACS inputs or result files were available to populate those directories without fabrication.

## 18. Limitations

- The original simulation directory was not present in the current workspace.
- No verified .mdp, .top, .gro, .edr, .xvg, or .png files were available for analysis in this environment.
- No production trajectory or energy analysis could be regenerated without rerunning the simulation.
- This repository is therefore a clean portfolio scaffold, not a reproduction of a previously completed public dataset.

## 19. Skills Demonstrated

This project is intended to demonstrate the following capabilities:

- Molecular dynamics simulation setup and execution
- Protein structure preparation and solvated-system construction
- Force-field-based simulation planning
- NVT and NPT equilibration workflows
- Production MD execution and system monitoring
- Trajectory analysis in GROMACS
- Structural interpretation of RMSD, RMSF, radius of gyration, and hydrogen bonds
- Scientific documentation and portfolio presentation for computational biology

## Repository Status

The production trajectory file `md.xtc` is intentionally excluded from the repository to avoid committing large simulation output while preserving the project structure and analysis-ready inputs. The current repository intentionally contains only the metadata and portfolio documentation required for a clean GitHub presentation.
