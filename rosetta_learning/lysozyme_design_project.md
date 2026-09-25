# Lysozyme as a Starter Rosetta Design Target

Lysozyme is a strong beginner project because it has a well-characterized catalytic site, a known fold, and a manageable design problem. It is also a useful portfolio target because it allows you to connect structure, chemistry, and mutation reasoning without starting from an extremely difficult enzyme family.

## Why lysozyme is a good first target

- well-studied catalytic active site
- clear relationship between structure and catalysis
- manageable substrate-binding pocket
- familiar to many protein design learners
- easy to communicate in a portfolio or interview setting

## Core design idea

The simplest learning question is:

> Can we identify a small number of residues near the catalytic site that could plausibly tune substrate binding or catalytic geometry without destabilizing the fold?

This is precisely the kind of question a Rosetta protein design workflow would ask.

## Relevant residues to investigate

In lysozyme, the catalytic site is centered around residues associated with the active-site machinery and surrounding pocket residues. A beginner project should focus on:

- catalytic or near-catalytic residues
- pocket-lining residues
- residues near substrate access routes
- solvent-exposed residues that may alter specificity or binding orientation

The first design cycle should not try to redesign the entire enzyme. Instead, start with a small set of candidate positions.

## Good first-round mutation strategy

For a lysozyme project, begin with mutations that are:

- conservative in size
- chemically reasonable
- close to the active site without being directly catalytic
- likely to change packing, polarity, or binding pocket geometry

Examples of design categories:

- hydrophobic-to-hydrophobic changes for tighter packing
- polar-to-polar changes for stronger H-bonding
- charge-preserving changes to tune electrostatics
- aromatic substitutions to alter aromatic stacking or pocket shape

## Example mutation hypotheses

These are example hypotheses for a beginner project, not claims that they are definitely optimal:

1. Conservative pocket redesign to improve packing near the substrate.
2. Add or remove a hydrogen bond near the catalytic region.
3. Alter aromatic content to change substrate orientation.
4. Tune a pocket entrance residue to affect access or specificity.
5. Rebalance charge near catalytic residues while preserving fold stability.

## Real Rosetta question to ask

A strong learning question is:

> Which 3-5 positions should I mutate first to test a pocket or specificity hypothesis, and why?

That is better than trying to produce a perfect redesign in one pass.

## Recommended workflow

1. Pick a lysozyme structure model.
2. Identify active-pocket and pocket-lining residues.
3. Build a small candidate library of 5-10 mutations.
4. Rank each mutation by:
   - proximity to catalytic region
   - likelihood of preserving fold
   - chemical plausibility
   - effect on hydrophobicity or charge
5. Draft a design memo for the best 3 mutations.
6. If Rosetta is available, turn the library into a fixbb or relax workflow.

## What a strong result looks like

Your final deliverable can be a short design brief that includes:

- target enzyme
- key catalytic and pocket residues
- 3-5 mutations under consideration
- rationale for each candidate
- one preferred variant
- one alternative variant
- one experimental validation plan

## Why this helps for your job search

This project demonstrates that you can:

- frame a protein-engineering problem
- reason about active-site chemistry
- build a candidate mutation library
- connect design ideas to Rosetta workflows
- communicate biologically grounded engineering decisions

That is exactly the kind of thinking the role description is asking for.
