# Rosetta Learning Project Plan

## Objective
Build a compact but realistic Rosetta study workflow that helps you learn the thinking behind enzyme design and computational protein engineering.

## 4-week plan

### Week 1: Foundations
Focus on structure and scoring intuition.

Tasks:
- Learn the Rosetta energy function at a conceptual level.
- Review protein structure basics: residues, side chains, packing, hydrogen bonds, active site geometry.
- Pick one enzyme target or scaffold to study.
- Create a list of catalytic, binding, and conserved residues.

Deliverable:
- one-page target summary with annotated residues

### Week 2: Design question and mutation library
Focus on creating a biologically anchored design problem.

Tasks:
- Define a question such as substrate specificity, pocket redesign, or catalytic stabilization.
- Build a mutation library of 5-10 candidate positions.
- Rank candidates by chemical and structural plausibility.

Deliverable:
- mutation library table with justifications

### Week 3: Rosetta workflow practice
If Rosetta is available, convert the mutation plan into protocol ideas.

Examples:
- fixbb for sequence redesign
- relax for local geometry optimization
- packer to optimize side-chain rotamers
- loopmodel for dynamic loop regions
- docking or interface design for complex systems

Deliverable:
- Rosetta command outline or design script

### Week 4: Interpretation and experimental proposal
Turn the results into a realistic engineering story.

Tasks:
- Compare variants by structural plausibility and residue compatibility.
- Note false positives and trade-offs.
- Draft a proposal for which mutants to test experimentally.

Deliverable:
- short design memo and prioritized experimental plan

## Suggested design questions

1. Can a substrate-binding residue be changed to increase specificity without destabilizing the pocket?
2. Is a catalytic residue too rigid or too solvent-exposed?
3. Which loop residues are most likely to affect access or orientation of a substrate?
4. Can an interface position be redesigned to increase binding selectivity without breaking fold stability?

## Good output to keep in your portfolio

- mutation library with rationale
- active-site annotation notes
- a comparison of candidate variants
- a short design memo that sounds like a real protein engineering plan

## What a strong final project looks like

It does not need to be a massive computational study. A strong project is one that clearly demonstrates:

- careful biological reasoning
- thoughtful mutation selection
- understanding of the structure-function link
- awareness of the limits of computational scoring

## Common mistakes to avoid

- Designing too many mutations at once
- Ignoring residue conservation and active-site chemistry
- Over-trusting raw energy scores without structural evaluation
- Treating a single Rosetta output as certainty
- Forgetting to connect the design to a measurable assay outcome

## Reflection questions

After each design cycle, ask:

- Why is this residue important?
- What is the likely trade-off of the mutation?
- Would I be comfortable defending this design in a lab meeting?
- What experiment would test the hypothesis fastest?
