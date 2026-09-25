# Rosetta Enzyme Design Learning Sandbox

This project is designed to help you build practical intuition for Rosetta-based protein design in the context of the role you shared: computational enzyme design, active-site engineering, rational mutagenesis, screening, and pathway-aware optimization.

The goal is not to replace a full Rosetta installation or a formal enzyme-design course. Instead, it gives you a structured sandbox for learning the concepts, building a repeatable workflow, and thinking like a protein designer.

## Why this project exists

For this role, the important skills are not only software commands but also the design logic:

- what makes a catalytic residue important
- how active-site geometry influences function
- how to think about mutation libraries
- how to evaluate a design before spending time on expensive wet-lab screening
- how to connect sequence changes to pathway and assay goals

This project helps you practice that reasoning with a realistic workflow.

## Learning goals

By the end of this study path, you should be able to:

1. Explain the difference between scoring, sampling, and design in Rosetta.
2. Recognize when to use a local refinement, loop modeling, docking, or interface design workflow.
3. Translate a biological problem into a mutagenesis plan.
4. Build a logically defensible design hypothesis for an enzyme active site.
5. Interpret Rosetta outputs without over-trusting a single score.

## Core Rosetta ideas to understand

### 1. Score function
Rosetta uses a physics-inspired energy function to approximate the favorability of a protein structure. This includes van der Waals, electrostatics, hydrogen bonding, solvation, and torsional terms.

When learning, ask:

- Does a mutation improve packing or worsen it?
- Does it create a favorable hydrogen bond or create strain?
- Is the change too solvent-exposed or too buried?
- Does the design preserve the overall fold while targeting the active site?

### 2. Sampling
Design is not just scoring a single structure. Rosetta explores many conformations and sequence possibilities. The key questions are:

- Are we sampling backbone flexibility or just side-chain rotamers?
- Are we optimizing a whole active site or only one residue?
- Are we using a local refinement model or a global design search?

### 3. Design logic
A strong design plan starts from biology, not from a score alone. The design question is usually something like:

- How do we stabilize the catalytic transition state?
- How do we remove an undesired substrate preference?
- How do we increase specificity without harming fold stability?
- How do we reduce a known catalytic bottleneck?

## Suggested mini-projects

### Mini-project A: Active-site redesign for substrate specificity
Use a known enzyme scaffold and ask:

- Which residues contact the substrate?
- Which positions are near the catalytic center?
- Which substitutions could improve packing or electrostatics?

Output: a ranked mutant list with a rationale for each position.

### Mini-project B: Loop and pocket optimization
Focus on a dynamic loop or an enzyme pocket. Ask:

- Does the loop need to open, close, or become more rigid?
- Which residues are likely to tune substrate access?
- What mutations may stabilize the productive conformation?

### Mini-project C: Interface design and allostery
If the target is enzyme engineering in a multicomponent system:

- identify interface residues
- assess electrostatic complementarity
- design changes that preserve binding but improve orientation or specificity

### Mini-project D: Mutational scanning and design prioritization
Generate a list of possible mutations and rank them according to:

- conservation
- chemical plausibility
- structural context
- likely catalytic impact

This mirrors the screening and mutagenesis thinking in the role description.

## Practical workflow for your learning

1. Choose a target enzyme or scaffold.
2. Read the structure and annotate residues:
   - catalytic residues
   - ligand-contacting residues
   - conserved residues
   - flexible or solvent-exposed loops
3. Build a design question.
   Example: “Can we increase specificity by changing a substrate-binding pocket residue without destabilizing the scaffold?”
4. Make a small mutation library.
   Limit to 3-10 candidates to keep the problem tractable.
5. Score and compare designs.
   Look at structural plausibility, not only total score.
6. Rank hypotheses.
   Favor designs with a clear biological explanation.
7. Translate to an experimental plan.
   Which variants should be made first? Which are low-confidence and should be left for later?

## Project structure

```text
rosetta_learning/
├── README.md
├── requirements.txt
├── project_plan.md
├── src/
│   ├── rosetta_learning.py
│   └── design_exercise.py
└── ideas/
    └── design_brainstorm.md
```

## Getting started

### Option 1: Learn conceptually without Rosetta installed
This repository is designed so you can work through the reasoning, mutation design, and project planning even before running a full Rosetta installation.

### Option 2: Use a local Rosetta environment
If you have access to a Rosetta install, you can convert the exercises here into actual Rosetta protocol commands such as:

- fixbb
- packer
- relax
- docking
- loopmodel
- enzyme_design

## Recommended study order

1. Read this README and the project plan.
2. Use the mutation-ranking scripts in `src/` to think about residues and candidates.
3. Create a small biological design target.
4. Write a one-page design brief for a hypothetical mutant library.
5. If Rosetta is available, turn that brief into a Rosetta command set.

## Brainstorm: design questions to explore

Use these as prompts for your own project work:

- Which active-site residues likely control substrate preference?
- Which mutations could increase catalytic efficiency without destabilizing the fold?
- Are there obvious trade-offs between stability and specificity?
- How do you decide whether a residue should be kept conserved or redesigned?
- What assay would validate the design concept in a real experimental pipeline?

## Important mindset

The key skill in protein design is not “generate a perfect score.” It is “form a strong hypothesis and test it intelligently.”

In Rosetta, a score can help you compare variants, but a good design still needs:

- biological plausibility
- structural reasoning
- a clear experimental follow-up
- awareness of trade-offs and uncertainty

## Next step

Start with the mutation exercise in `src/design_exercise.py` and use it to draft a small enzyme-design proposal. That will help you connect Rosetta concepts to the actual type of work described in the role.
