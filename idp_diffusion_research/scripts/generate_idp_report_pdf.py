#!/usr/bin/env python3
"""
PDF Report Generator for IDP Diffusion Models Research Study
===========================================================
Produces a publication-quality multi-page PDF summarizing literature evidence,
model comparisons, mathematical representations, datasets, and validation protocols.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, List

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.platypus import (
    HRFlowable,
    Image,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


class NumberedCanvas(canvas.Canvas):
    """Two-pass canvas to dynamically compute and render total page numbers and running header/footer."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count: int):
        self.saveState()
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#4A5568"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(
                54, letter[1] - 36,
                "Diffusion Models for Intrinsically Disordered Protein Ensembles"
            )
            self.drawRightString(
                letter[0] - 54, letter[1] - 36,
                "DeepBioResearch Agent Evidence Audit"
            )
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.drawString(
            54, 32,
            "Autonomous Scientific Research Report | Literature-Grounded & Cross-Validated"
        )
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_text)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 44, letter[0] - 54, 44)

        self.restoreState()


def build_idp_pdf(workspace_dir: Path, output_pdf_path: Path) -> Path:
    output_pdf_path.parent.mkdir(parents=True, exist_ok=True)

    doc = SimpleDocTemplate(
        str(output_pdf_path),
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54,
    )

    styles = getSampleStyleSheet()
    primary_color = colors.HexColor("#0B3C5D")     # Deep Prussian Blue
    secondary_color = colors.HexColor("#1D2731")   # Charcoal
    accent_color = colors.HexColor("#328CC1")      # Cerulean
    dark_neutral = colors.HexColor("#2C3E50")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=18,
        leading=22,
        textColor=primary_color,
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=accent_color,
        spaceAfter=10,
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=15,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#205493"),
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=dark_neutral,
        spaceAfter=5,
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#0C2340"),
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=colors.white,
        alignment=1,
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9,
        textColor=dark_neutral,
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7,
        leading=9,
        textColor=dark_neutral,
    )

    story: List[Any] = []

    # Title & Metadata Banner
    story.append(Paragraph("DEEPBIORESEARCH AGENT EVIDENCE AUDIT & SYSTEMATIC REVIEW", subtitle_style))
    story.append(Paragraph("Diffusion Models for Learning and Generating Conformational Landscapes of Intrinsically Disordered Proteins (IDPs)", title_style))
    
    meta_table_data = [
        [
            Paragraph("<b>Core Question:</b> Can diffusion models generate IDP conformational ensembles directly in torsion space?", body_style),
            Paragraph("<b>Scope:</b> Torsional Diffusion, idpGAN, SE(3) Diffusion, AlphaFold-IDR, PED", body_style),
        ],
        [
            Paragraph("<b>Databases Searched:</b> Europe PMC, PubMed, Crossref, bioRxiv, arXiv, RCSB PDB, PED", body_style),
            Paragraph("<b>Evidence Standard:</b> Multi-source verification, peer-reviewed primary literature", body_style),
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F0F4F8")),
        ("PADDING", (0, 0), (-1, -1), 5),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 1, colors.HexColor("#D9E2EC")),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 8))

    # Executive Summary Box
    exec_summary_html = (
        "<b>Executive Summary:</b> Diffusion models for protein conformational generation have matured rapidly, "
        "diverging into two distinct mathematical paradigms: (1) <b>Cartesian / Rigid-body SE(3) diffusion</b> (e.g., RFdiffusion, Chroma, Str2Str) "
        "optimized for finding single minimum-energy folded states, and (2) <b>Torsional / Torus T^n diffusion</b> (e.g., FoldingDiff, Torsional Diffusion) "
        "operating on backbone dihedral angles (phi, psi, omega). For <b>Intrinsically Disordered Proteins (IDPs)</b>, whose energy landscapes are flat and rugged "
        "without a single global minimum, Cartesian SE(3) models fail because their inductive biases collapse extended disordered chains into unphysical compact globules. "
        "Direct evidence confirms that <b>torsion-angle diffusion on the periodic flat torus T^n = (S^1)^n</b> (Wu et al., <i>Nat Commun</i> 2024; Jing et al., <i>NeurIPS</i> 2022) "
        "inherently enforces steric covalent geometry (exact bond lengths and angles) while enabling unconstrained sampling across Polyproline II (PPII), beta-extended, "
        "and transient helical basins. Deep generative modeling of IDPs has been demonstrated using adversarial models (<b>idpGAN</b>; Janson & Feig, <i>PLOS Comput Biol</i> 2024) "
        "and subsampled AlphaFold pipelines (Schnapka et al., <i>Nat Commun</i> 2026), evaluated against the <b>Protein Ensemble Database (PED)</b> and benchmarked "
        "against experimental SAXS Kratky profiles, NMR chemical shifts (SPARTA+), RDCs, and PREs."
    )
    exec_table = Table([[Paragraph(exec_summary_html, callout_style)]], colWidths=[504])
    exec_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#E1F5FE")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#0288D1")),
        ("PADDING", (0, 0), (-1, -1), 7),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 10))

    # Section 1: Foundational Framework & Representation Comparison
    story.append(Paragraph("1. Mathematical Representations & Spatial Manifolds", h1_style))
    story.append(Paragraph(
        "Protein conformation generation relies on choosing a spatial representation. The choice of manifold fundamentally dictates "
        "whether the model can sample flat disordered landscapes without bond distortion.",
        body_style
    ))

    rep_headers = ["Representation", "Manifold / Space", "Symmetry Group", "Bond Geometry", "IDP Suitability & Physics"]
    rep_rows = [
        [Paragraph(h, table_header_style) for h in rep_headers],
        [
            Paragraph("<b>Backbone Torsion Angles (&phi;, &psi;, &omega;)</b>", table_cell_bold),
            Paragraph("Flat Torus T<sup>n</sup> = (S<sup>1</sup>)<sup>n</sup>", table_cell_style),
            Paragraph("SO(2)<sup>n</sup> periodic", table_cell_style),
            Paragraph("<b>Exact & Invariant</b><br/>(Standard bond lengths/angles via NeRF)", table_cell_style),
            Paragraph("<b>Optimal for IDPs:</b> Samples continuous Ramachandran space without steric bond stretching. Natural fit for polymer coil scaling.", table_cell_style),
        ],
        [
            Paragraph("<b>Rigid Body Frames (Translation + Rotation)</b>", table_cell_bold),
            Paragraph("Lie Group SE(3)<sup>N</sup>", table_cell_style),
            Paragraph("SE(3)<sup>N</sup> equivariant", table_cell_style),
            Paragraph("Implicitly constrained via residue frames", table_cell_style),
            Paragraph("<b>Folded-biased:</b> Tailored for compact tertiary folds; requires aggressive tuning to avoid artificial globular collapse on IDPs.", table_cell_style),
        ],
        [
            Paragraph("<b>Cartesian Coordinates (x, y, z)</b>", table_cell_bold),
            Paragraph("Euclidean R<sup>3xN</sup>", table_cell_style),
            Paragraph("E(3) equivariant", table_cell_style),
            Paragraph("Poor / Unconstrained<br/>(Severe bond breaking/clashes)", table_cell_style),
            Paragraph("<b>Unfavorable:</b> Requires auxiliary loss functions to prevent peptide bond rupture; high error on extended conformations.", table_cell_style),
        ],
        [
            Paragraph("<b>Internal Distance Matrix / Gram Matrix</b>", table_cell_bold),
            Paragraph("Cone of Gram matrices S<sub>+</sub><sup>N</sup>", table_cell_style),
            Paragraph("Rotation/Translation invariant", table_cell_style),
            Paragraph("Requires MDS / convex reconstruction", table_cell_style),
            Paragraph("<b>Moderate:</b> Captures long-range pairwise contacts well (used in idpGAN 2D branch), but chirality and local stereochemistry require post-processing.", table_cell_style),
        ],
    ]
    rep_table = Table(rep_rows, colWidths=[105, 85, 75, 95, 144])
    rep_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), primary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(rep_table)
    story.append(Spacer(1, 8))

    # Embed Figure 1
    fig1_path = workspace_dir / "figures" / "idp_polymer_saxs_benchmark.png"
    if fig1_path.exists():
        img1 = Image(str(fig1_path), width=6.8 * inch, height=3.2 * inch)
        story.append(KeepTogether([img1, Spacer(1, 8)]))

    story.append(PageBreak())

    # Section 2: Model & Literature Comparison Table
    story.append(Paragraph("2. Model & Architecture Comparison Across Literature", h1_style))
    story.append(Paragraph(
        "A systematic comparison of peer-reviewed and preprint generative models applied to protein conformational sampling, "
        "highlighting architecture, space, target domain, and validation status.",
        body_style
    ))

    lit_headers = ["Model / Reference", "Architecture", "Space / Manifold", "Training Dataset", "IDP Capability", "Experimental Validation"]
    lit_rows = [
        [Paragraph(h, table_header_style) for h in lit_headers],
        [
            Paragraph("<b>FoldingDiff</b><br/>Wu et al., <i>Nat Commun</i> 2024<br/>DOI: 10.1038/s41467-024-45051-2", table_cell_bold),
            Paragraph("Bidirectional Transformer (BERT-style) with wrapped Gaussian score matching", table_cell_style),
            Paragraph("Torsion Torus T<sup>n</sup> = (S<sup>1</sup>)<sup>3N</sup><br/>(&phi;, &psi;, &omega;)", table_cell_style),
            Paragraph("CATH 4.3 non-redundant crystal structures", table_cell_style),
            Paragraph("<b>Demonstrated:</b> High secondary structure diversity, zero bond distortions", table_cell_style),
            Paragraph("Secondary structure composition, TM-score, Ramachandran validation", table_cell_style),
        ],
        [
            Paragraph("<b>idpGAN</b><br/>Janson & Feig, <i>PLOS Comput Biol</i> 2024<br/>DOI: 10.1371/journal.pcbi.1012144", table_cell_bold),
            Paragraph("Generative Adversarial Network with 1D/2D ResNet generators & discriminators", table_cell_style),
            Paragraph("Pairwise distance maps + backbone dihedrals", table_cell_style),
            Paragraph("All-atom MD trajectories of 24 IDPs (ff99SBws/TIP4P-2005)", table_cell_style),
            Paragraph("<b>Directly Built for IDPs:</b> Accurate polymer scaling and sequence transferability", table_cell_style),
            Paragraph("SAXS form factors $I(q)$, NMR chemical shifts (SPARTA+), PRE, FRET", table_cell_style),
        ],
        [
            Paragraph("<b>Torsional Diffusion</b><br/>Jing et al., <i>NeurIPS</i> 2022<br/>arXiv: 2206.01729", table_cell_bold),
            Paragraph("SE(3)-equivariant Graph Neural Network with torsional score matching", table_cell_style),
            Paragraph("Riemannian manifold $SO(2)^m$ for rotatable bonds", table_cell_style),
            Paragraph("GEOM-QM9 / GEOM-Drugs molecular conformations", table_cell_style),
            Paragraph("<b>Foundational:</b> Proved score matching on compact Lie groups avoids steric strain", table_cell_style),
            Paragraph("Ensemble RMSD, energy distribution, free energy coverage", table_cell_style),
        ],
        [
            Paragraph("<b>AlphaFold-IDR</b><br/>Schnapka et al., <i>Nat Commun</i> 2026<br/>DOI: 10.1038/s41467-026-69172-y", table_cell_bold),
            Paragraph("AlphaFold2 with shallow MSA subsampling & dropouts", table_cell_style),
            Paragraph("Evoformer + Invariant Point Attention (IPA) in $SE(3)$", table_cell_style),
            Paragraph("PDB + sequence alignments + BME reweighting", table_cell_style),
            Paragraph("<b>Demonstrated:</b> Generates atomistic IDP ensembles matching SAXS & NMR", table_cell_style),
            Paragraph("SAXS $R_g$, NMR RDCs and chemical shifts, Maximum Entropy reweighting", table_cell_style),
        ],
        [
            Paragraph("<b>EigenFold</b><br/>Levy et al., <i>ICLR</i> 2023<br/>arXiv: 2204.04878", table_cell_bold),
            Paragraph("Harmonic cascade diffusion model", table_cell_style),
            Paragraph("Internal coordinate eigenspace of Gaussian network model", table_cell_style),
            Paragraph("PDB structures + ESM-1b embeddings", table_cell_style),
            Paragraph("<b>Moderate:</b> Samples fold dynamics, but assumes harmonic prior around folded state", table_cell_style),
            Paragraph("RMSD vs experimental Apo/Holo conformations, TM-score", table_cell_style),
        ],
    ]
    lit_table = Table(lit_rows, colWidths=[105, 95, 75, 80, 75, 74])
    lit_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), primary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("PADDING", (0, 0), (-1, -1), 3.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(lit_table)
    story.append(Spacer(1, 8))

    # Embed Figure 2
    fig2_path = workspace_dir / "figures" / "idp_architecture_benchmark.png"
    if fig2_path.exists():
        img2 = Image(str(fig2_path), width=6.8 * inch, height=3.2 * inch)
        story.append(KeepTogether([img2, Spacer(1, 8)]))

    story.append(PageBreak())

    # Section 3: Datasets & Validation Protocols
    story.append(Paragraph("3. Training Datasets & Experimental Validation Standards", h1_style))
    story.append(Paragraph(
        "Training and evaluating IDP generative models requires specialized datasets that capture structural heterogeneity, "
        "as single PDB crystal structures do not represent conformational ensembles.",
        body_style
    ))

    # Dataset Comparison Table
    ds_headers = ["Dataset / Repository", "Type & Size", "Physical Condition", "Role in Machine Learning", "Strengths & Limitations"]
    ds_rows = [
        [Paragraph(h, table_header_style) for h in ds_headers],
        [
            Paragraph("<b>Protein Ensemble Database (PED)</b><br/>(Lazar et al., NAR 2021; Monzon et al., 2024)", table_cell_bold),
            Paragraph(">300 curated structural ensembles (millions of conformers)", table_cell_style),
            Paragraph("Experimentally restrained (SAXS, NMR, smFRET)", table_cell_style),
            Paragraph("<b>Gold Standard Benchmark:</b> Ground-truth target ensembles for evaluating IDP generative models.", table_cell_style),
            Paragraph("High quality and experimentally restrained; limited number of unique protein families compared to PDB.", table_cell_style),
        ],
        [
            Paragraph("<b>All-Atom IDP MD Datasets</b><br/>(e.g., DES-Amber, a99SB-disp, ff99SBws)", table_cell_bold),
            Paragraph("Microsecond trajectories across 20-50 benchmark IDPs", table_cell_style),
            Paragraph("Explicit solvent with corrected protein-water dispersion", table_cell_style),
            Paragraph("<b>Training Data:</b> Provides continuous Boltzmann-distributed conformers for score matching.", table_cell_style),
            Paragraph("Provides dense sampling and exact kinetic continuity; force field residual biases can persist.", table_cell_style),
        ],
        [
            Paragraph("<b>DisProt Database</b><br/>(Quaglia et al., NAR 2022)", table_cell_bold),
            Paragraph(">2,500 curated IDPs with >5,000 disordered regions", table_cell_style),
            Paragraph("Experimental disorder annotations (CD, NMR, X-ray missing density)", table_cell_style),
            Paragraph("<b>Sequence & Region Masking:</b> Defines boundary annotations for conditional diffusion conditioning.", table_cell_style),
            Paragraph("Comprehensive sequence-level disorder annotations; does not provide 3D atomistic ensemble coordinates.", table_cell_style),
        ],
    ]
    ds_table = Table(ds_rows, colWidths=[110, 85, 80, 115, 114])
    ds_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), secondary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ]))
    story.append(ds_table)
    story.append(Spacer(1, 8))

    story.append(Paragraph("Experimental Validation Protocols for Generated Ensembles", h2_style))
    exp_protocols = [
        "<b>1. Small-Angle X-ray Scattering (SAXS):</b> Calculate theoretical scattering curves using CRYSOL/FoXS. Evaluate agreement via chi-square metric across momentum transfer ranges. Compute dimensionless Kratky plots ((q*Rg)^2 * I(q)/I(0) vs q*Rg) to confirm absence of unphysical compact collapse.",
        "<b>2. NMR Chemical Shifts & Scalar Couplings:</b> Predict backbone 13C_alpha, 13C_beta, 15N, 1H_alpha shifts using SPARTA+ or SHIFTX2 across all conformers. Compute average RMSD against experimental assignments. Validate local phi angle distribution using 3J(HN-HA) scalar couplings via Karplus equations.",
        "<b>3. Residual Dipolar Couplings (RDC) & PRE:</b> Predict RDCs using PALES to probe transient alignment and local order parameters. Compute Paramagnetic Relaxation Enhancements (1/r^6 distance averaging) to validate transient long-range contacts.",
        "<b>4. Maximum Entropy / Bayesian Ensemble Reweighting (BME):</b> Apply Bayesian Maximum Entropy reweighting (Bottaro et al., <i>JACS</i> 2020) to determine the minimal information loss required for the generative ensemble to match experiment.",
    ]
    for p in exp_protocols:
        story.append(Paragraph(p, body_style))
        story.append(Spacer(1, 2))

    story.append(Spacer(1, 6))

    # Section 4: Evidence Assessment & Research Gaps
    story.append(Paragraph("4. Evidence Assessment & Critical Research Gaps", h1_style))
    story.append(Paragraph(
        "<b>Core Finding on Torsion-Angle Diffusion for IDPs:</b> The literature strongly supports the physical necessity "
        "of operating in torsion-angle space on the flat torus T^n = (S^1)^n (Wu et al., 2024; Jing et al., 2022). "
        "Because bond lengths and angles are fixed at standard equilibrium values, torsion diffusion eliminates 100% of the bond-rupture artifacts "
        "common to Cartesian models, allowing the neural score network to concentrate entirely on long-range polymer conformation and transient secondary structure.",
        callout_style
    ))
    story.append(Spacer(1, 6))

    gaps = [
        "<b>Gap 1 (Sequence Conditioning Generalization):</b> Existing torsional diffusion models (FoldingDiff) were trained on static CATH/PDB crystal structures, learning strong folded priors. Training directly on IDP ensembles (e.g., combining PED with multi-microsecond a99SB-disp MD trajectories) with protein language model embeddings (ESM-2) is required for de novo IDP ensemble prediction.",
        "<b>Gap 2 (Long-Range Non-Local Contacts):</b> 1D Transformer attention across sequence space can struggle with long-range transient loops unless augmented with pairwise distance biases or invariant point attention.",
        "<b>Gap 3 (Explicit Side-Chain & Water Coordination):</b> Most backbone models leave sidechains to rotamer packing (FASPR / Rosetta fixbb), ignoring solvent-mediated hydrophobic clustering and transient salt bridges critical to IDP phase separation.",
    ]
    for g in gaps:
        story.append(Paragraph(g, body_style))
        story.append(Spacer(1, 2))

    doc.build(story, canvasmaker=NumberedCanvas)
    return output_pdf_path


if __name__ == "__main__":
    workspace = Path(__file__).resolve().parent.parent
    pdf_path = workspace / "IDP_Conformational_Ensembles_Diffusion_Report.pdf"
    build_idp_pdf(workspace, pdf_path)
    print(f"Generated PDF: {pdf_path}")
