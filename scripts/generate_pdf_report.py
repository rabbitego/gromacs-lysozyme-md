#!/usr/bin/env python3
"""
Research-Grade PDF Report Generator for Lysozyme MD & Rosetta Enzyme Design
==========================================================================
Generates a publication-quality multi-page PDF report with embedded high-DPI
figures, formatted statistical data tables, and experimental translation plans.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import List

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
                "HEWL (1AKI) Biophysics & Rational Enzyme Design Report"
            )
            self.drawRightString(
                letter[0] - 54, letter[1] - 36,
                "Computational Biochemistry Pipeline"
            )
            self.setStrokeColor(colors.HexColor("#CBD5E0"))
            self.setLineWidth(0.5)
            self.line(54, letter[1] - 42, letter[0] - 54, letter[1] - 42)

        # Footer (all pages)
        self.setFont("Helvetica", 8)
        self.drawString(
            54, 32,
            "Confidential - Research & Protein Engineering Report | Target PDB: 1AKI (EC 3.2.1.17)"
        )
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(letter[0] - 54, 32, page_text)
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.5)
        self.line(54, 44, letter[0] - 54, 44)

        self.restoreState()


def build_pdf_report(workspace_dir: Path, output_pdf_path: Path) -> Path:
    """Build the comprehensive research PDF report."""
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

    # Custom typography styles
    primary_color = colors.HexColor("#0F2942")     # Deep Navy
    secondary_color = colors.HexColor("#1A5276")   # Slate Blue
    accent_color = colors.HexColor("#D35400")      # Rust / Orange
    dark_neutral = colors.HexColor("#2C3E50")
    light_bg = colors.HexColor("#F8F9FA")

    title_style = ParagraphStyle(
        "DocTitle",
        parent=styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=primary_color,
        spaceAfter=6,
    )

    subtitle_style = ParagraphStyle(
        "DocSubTitle",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=15,
        textColor=secondary_color,
        spaceAfter=12,
    )

    h1_style = ParagraphStyle(
        "SectionH1",
        parent=styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=13,
        leading=16,
        textColor=primary_color,
        spaceBefore=12,
        spaceAfter=6,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "SectionH2",
        parent=styles["Heading3"],
        fontName="Helvetica-Bold",
        fontSize=10.5,
        leading=13,
        textColor=secondary_color,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "BodyDark",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=9,
        leading=12.5,
        textColor=dark_neutral,
        spaceAfter=6,
    )

    callout_style = ParagraphStyle(
        "CalloutText",
        parent=styles["Normal"],
        fontName="Helvetica-Oblique",
        fontSize=8.5,
        leading=12,
        textColor=colors.HexColor("#1C3D5A"),
    )

    table_header_style = ParagraphStyle(
        "TableHeader",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=8,
        leading=10,
        textColor=colors.white,
        alignment=1,  # Center
    )

    table_cell_style = ParagraphStyle(
        "TableCell",
        parent=styles["Normal"],
        fontName="Helvetica",
        fontSize=7.5,
        leading=9.5,
        textColor=dark_neutral,
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.5,
        leading=9.5,
        textColor=dark_neutral,
    )

    story: List[Any] = []

    # =========================================================================
    # Header Banner & Title
    # =========================================================================
    story.append(Paragraph("RESEARCH SUMMARY & BIOPHYSICAL REPORT", subtitle_style))
    story.append(Paragraph("Hen Egg-White Lysozyme (HEWL): 10 ns All-Atom MD & Rosetta REF2015 Enzyme Redesign", title_style))
    
    meta_table_data = [
        [
            Paragraph("<b>Target System:</b> Hen Egg-White Lysozyme (HEWL, PDB: 1AKI)", body_style),
            Paragraph("<b>Enzyme Commission:</b> EC 3.2.1.17 (Hydrolase)", body_style),
        ],
        [
            Paragraph("<b>Simulation Protocol:</b> AMBER99SB-ILDN / TIP3P, NPT (300 K, 1 bar)", body_style),
            Paragraph("<b>Design Methodology:</b> Rosetta REF2015 & Pareto Multi-Objective Optimization", body_style),
        ]
    ]
    meta_table = Table(meta_table_data, colWidths=[250, 254])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EDF2F7")),
        ("PADDING", (0, 0), (-1, -1), 6),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LINEBELOW", (0, 0), (-1, -1), 1, colors.HexColor("#CBD5E0")),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 10))

    # =========================================================================
    # Executive Summary Box
    # =========================================================================
    exec_summary_html = (
        "<b>Executive Summary:</b> This study presents an integrated computational biophysics investigation "
        "coupling a 10 ns all-atom Molecular Dynamics (MD) trajectory with Rosetta REF2015 rational enzyme engineering. "
        "Equilibrium trajectories confirmed high globular stability (Cα RMSD = 0.153 ± 0.015 nm, Rg = 1.418 ± 0.007 nm, "
        "and 101.84 ± 4.45 intramolecular H-bonds) with rigid catalytic dyad anchors (Glu35 RMSF = 0.0435 nm, Asp52 RMSF = 0.0573 nm). "
        "Subsite-specific mutational remodeling identified Pareto-optimal candidates <b>Asp101Asn (M2)</b> (ΔΔG_fold = -3.06 REU, -1.99 kcal/mol), "
        "<b>Trp62Tyr (M1)</b> (ΔΔG_fold = -2.28 REU, -1.48 kcal/mol), and <b>Arg45Lys (M5)</b> (ΔΔG_fold = -1.44 REU, -0.93 kcal/mol), "
        "which successfully tune subsite carbohydrate recognition while rigorously conserving catalytic transition-state geometry."
    )
    exec_table = Table([[Paragraph(exec_summary_html, callout_style)]], colWidths=[504])
    exec_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#EBF8FF")),
        ("BOX", (0, 0), (-1, -1), 1, colors.HexColor("#3182CE")),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    story.append(exec_table)
    story.append(Spacer(1, 12))

    # =========================================================================
    # Section 1: Molecular Dynamics Trajectory Validation
    # =========================================================================
    story.append(Paragraph("1. Molecular Dynamics Trajectory & Statistical Mechanics", h1_style))
    story.append(Paragraph(
        "A 10 ns production trajectory (5,000,000 steps, dt = 2 fs) was analyzed using autocorrelation correction (N_eff) "
        "and block averaging to ensure statistical independence and stationarity across all thermodynamic observables.",
        body_style
    ))

    # Summary Metrics Table
    md_headers = ["Observable", "Symbol", "Mean ± Std", "SEM", "95% Conf. Interval", "Physical Status"]
    md_rows = [
        [Paragraph(h, table_header_style) for h in md_headers],
        [Paragraph("Backbone Cα RMSD", table_cell_bold), Paragraph("RMSD", table_cell_style), Paragraph("0.153 ± 0.015 nm", table_cell_style), Paragraph("0.0042 nm", table_cell_style), Paragraph("[0.144, 0.161] nm", table_cell_style), Paragraph("Converged (1.53 Å)", table_cell_style)],
        [Paragraph("Radius of Gyration", table_cell_bold), Paragraph("Rg", table_cell_style), Paragraph("1.418 ± 0.007 nm", table_cell_style), Paragraph("0.0007 nm", table_cell_style), Paragraph("[1.417, 1.420] nm", table_cell_style), Paragraph("Stable Compact Fold", table_cell_style)],
        [Paragraph("Shape Anisotropy", table_cell_bold), Paragraph("κ²", table_cell_style), Paragraph("0.018 ± 0.005", table_cell_style), Paragraph("0.0006", table_cell_style), Paragraph("[0.017, 0.019]", table_cell_style), Paragraph("Prolate Spheroid", table_cell_style)],
        [Paragraph("Intramolecular H-Bonds", table_cell_bold), Paragraph("N_HB", table_cell_style), Paragraph("101.84 ± 4.45", table_cell_style), Paragraph("0.44 count", table_cell_style), Paragraph("[100.97, 102.71]", table_cell_style), Paragraph("Native α/β Network", table_cell_style)],
        [Paragraph("System Temperature", table_cell_bold), Paragraph("T", table_cell_style), Paragraph("300.02 ± 1.68 K", table_cell_style), Paragraph("0.17 K", table_cell_style), Paragraph("[299.69, 300.35] K", table_cell_style), Paragraph("Equilibrium (300 K)", table_cell_style)],
        [Paragraph("Ensemble Pressure", table_cell_bold), Paragraph("P", table_cell_style), Paragraph("1.29 ± 153.2 bar", table_cell_style), Paragraph("15.3 bar", table_cell_style), Paragraph("[-28.7, 31.3] bar", table_cell_style), Paragraph("Normal MD Virial", table_cell_style)],
        [Paragraph("Solvent Density", table_cell_bold), Paragraph("ρ", table_cell_style), Paragraph("992.35 ± 4.48 kg/m³", table_cell_style), Paragraph("0.45 kg/m³", table_cell_style), Paragraph("[991.47, 993.23] kg/m³", table_cell_style), Paragraph("TIP3P Bulk Density", table_cell_style)],
    ]
    md_table = Table(md_rows, colWidths=[105, 45, 95, 60, 95, 104])
    md_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), primary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(md_table)
    story.append(Spacer(1, 10))

    # Embed MD Comprehensive Figure
    md_fig_path = workspace_dir / "figures" / "md_comprehensive_analysis.png"
    if md_fig_path.exists():
        img = Image(str(md_fig_path), width=6.8 * inch, height=6.2 * inch)
        story.append(KeepTogether([img, Spacer(1, 8)]))

    story.append(PageBreak())

    # =========================================================================
    # Section 2: Residue-Level Dynamics & Crystallographic B-Factors
    # =========================================================================
    story.append(Paragraph("2. Residue Dynamics, Crystallographic B-Factors & Subsite Anatomy", h1_style))
    story.append(Paragraph(
        "Local conformational fluctuations were calculated from Cα Root-Mean-Square Fluctuations (RMSF) and converted "
        "to theoretical crystallographic isotropic displacement parameters via the Debye-Waller relation "
        "<b>B_i = (8π²/3) · <Δr_i²> = (8π²/3) · (10 · RMSF_i)²</b>. "
        "The catalytic machinery exhibits remarkable structural rigidity compared to peripheral solvent-exposed loops.",
        body_style
    ))

    # Active site table
    as_headers = ["Functional Site / Region", "Key Residues", "RMSF (nm)", "B-factor (Å²)", "Biophysical Role"]
    as_rows = [
        [Paragraph(h, table_header_style) for h in as_headers],
        [Paragraph("Catalytic General Acid", table_cell_bold), Paragraph("Glu35", table_cell_style), Paragraph("0.0435 nm", table_cell_style), Paragraph("4.96 Å²", table_cell_style), Paragraph("Proton donor; elevated pKa (~6.2) in hydrophobic niche", table_cell_style)],
        [Paragraph("Catalytic Nucleophile", table_cell_bold), Paragraph("Asp52", table_cell_style), Paragraph("0.0573 nm", table_cell_style), Paragraph("8.63 Å²", table_cell_style), Paragraph("Oxocarbenium intermediate electrostatic stabilizer", table_cell_style)],
        [Paragraph("Subsite B Aromatic Clamp", table_cell_bold), Paragraph("Trp62, Trp63", table_cell_style), Paragraph("0.0460 nm", table_cell_style), Paragraph("5.56 Å²", table_cell_style), Paragraph("Carbohydrate CH-π stacking platform", table_cell_style)],
        [Paragraph("Subsite D Transition Floor", table_cell_bold), Paragraph("Trp108, Val109", table_cell_style), Paragraph("0.0422 nm", table_cell_style), Paragraph("4.68 Å²", table_cell_style), Paragraph("Steric crowding enforcing substrate ring boat distortion", table_cell_style)],
        [Paragraph("Subsite A Entrance Gate", table_cell_bold), Paragraph("Asp101, Asn103", table_cell_style), Paragraph("0.0468 nm", table_cell_style), Paragraph("5.75 Å²", table_cell_style), Paragraph("Electrostatic steering for glycan oligomers", table_cell_style)],
        [Paragraph("Subsite E Leaving Group", table_cell_bold), Paragraph("Arg45, Arg68", table_cell_style), Paragraph("0.0504 nm", table_cell_style), Paragraph("6.68 Å²", table_cell_style), Paragraph("Cationic steering channel at cleavage exit", table_cell_style)],
    ]
    as_table = Table(as_rows, colWidths=[115, 75, 55, 60, 199])
    as_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), secondary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(as_table)
    story.append(Spacer(1, 8))

    # Embed RMSF & B-factor Figure
    rmsf_fig_path = workspace_dir / "figures" / "rmsf_bfactor_landscape.png"
    if rmsf_fig_path.exists():
        img_b = Image(str(rmsf_fig_path), width=6.8 * inch, height=4.2 * inch)
        story.append(KeepTogether([img_b, Spacer(1, 8)]))

    story.append(PageBreak())

    # =========================================================================
    # Section 3: Rosetta REF2015 Mutational Design & Pareto Optimization
    # =========================================================================
    story.append(Paragraph("3. Rosetta REF2015 Mutational Design & Pareto Frontier", h1_style))
    story.append(Paragraph(
        "Candidate mutations targeting subsites A through E were evaluated using the full <b>REF2015</b> scoring potential. "
        "Multi-objective Pareto optimization simultaneously considered folding stability (ΔΔG_fold), substrate binding affinity (ΔΔG_bind), "
        "and catalytic dyad coordinate conservation.",
        body_style
    ))

    # Mutant evaluation table
    mut_headers = ["ID", "Mutation", "Subsite", "ΔΔG_fold (REU)", "ΔΔG (kcal/mol)", "ΔΔG_bind (REU)", "CatScore", "Pareto Status", "Design Rationale"]
    mut_rows = [
        [Paragraph(h, table_header_style) for h in mut_headers],
        [Paragraph("M2", table_cell_bold), Paragraph("D101N", table_cell_bold), Paragraph("Subsite A", table_cell_style), Paragraph("<b>-3.06</b>", table_cell_style), Paragraph("-1.99", table_cell_style), Paragraph("-1.95", table_cell_style), Paragraph("1.00", table_cell_style), Paragraph("<font color='#2E7D32'><b>Optimal (Rank 1)</b></font>", table_cell_style), Paragraph("Removes charge repulsion with deacetylated glycan", table_cell_style)],
        [Paragraph("M1", table_cell_bold), Paragraph("W62Y", table_cell_bold), Paragraph("Subsite B", table_cell_style), Paragraph("<b>-2.28</b>", table_cell_style), Paragraph("-1.48", table_cell_style), Paragraph("-1.35", table_cell_style), Paragraph("0.98", table_cell_style), Paragraph("<font color='#2E7D32'><b>Optimal (Rank 2)</b></font>", table_cell_style), Paragraph("Tunes aromatic clamp footprint; adds phenolic H-bond", table_cell_style)],
        [Paragraph("M5", table_cell_bold), Paragraph("R45K", table_cell_bold), Paragraph("Subsite E", table_cell_style), Paragraph("<b>-1.44</b>", table_cell_style), Paragraph("-0.93", table_cell_style), Paragraph("-0.85", table_cell_style), Paragraph("0.99", table_cell_style), Paragraph("<font color='#2E7D32'><b>Optimal (Rank 3)</b></font>", table_cell_style), Paragraph("Conserves basic steering with lower steric volume", table_cell_style)],
        [Paragraph("M4", table_cell_bold), Paragraph("N59S", table_cell_style), Paragraph("Subsite B/C", table_cell_style), Paragraph("-0.90", table_cell_style), Paragraph("-0.58", table_cell_style), Paragraph("-0.55", table_cell_style), Paragraph("0.99", table_cell_style), Paragraph("Non-Dominated", table_cell_style), Paragraph("Cleft rim widening for bulky/branched polymers", table_cell_style)],
        [Paragraph("M7", table_cell_bold), Paragraph("A107G", table_cell_style), Paragraph("Subsite C", table_cell_style), Paragraph("-0.34", table_cell_style), Paragraph("-0.22", table_cell_style), Paragraph("-0.40", table_cell_style), Paragraph("0.96", table_cell_style), Paragraph("Non-Dominated", table_cell_style), Paragraph("Increases cleft floor backbone flexibility", table_cell_style)],
        [Paragraph("M8", table_cell_bold), Paragraph("I98V", table_cell_style), Paragraph("Subsite C", table_cell_style), Paragraph("-0.18", table_cell_style), Paragraph("-0.12", table_cell_style), Paragraph("-0.25", table_cell_style), Paragraph("0.99", table_cell_style), Paragraph("Non-Dominated", table_cell_style), Paragraph("Conservative cavity-creating packing tuner", table_cell_style)],
        [Paragraph("M3", table_cell_bold), Paragraph("W108F", table_cell_style), Paragraph("Subsite D", table_cell_style), Paragraph("+1.31", table_cell_style), Paragraph("+0.85", table_cell_style), Paragraph("+0.80", table_cell_style), Paragraph("0.72", table_cell_style), Paragraph("Mechanistic Probe", table_cell_style), Paragraph("Relieves subsite D strain; alters sugar distortion", table_cell_style)],
        [Paragraph("M6", table_cell_bold), Paragraph("D52E", table_cell_style), Paragraph("Active Site", table_cell_style), Paragraph("+3.47", table_cell_style), Paragraph("+2.26", table_cell_style), Paragraph("+2.10", table_cell_style), Paragraph("0.05", table_cell_style), Paragraph("<font color='#C62828'><b>Negative Control</b></font>", table_cell_style), Paragraph("Destroys catalytic carboxylate TS alignment", table_cell_style)],
    ]
    mut_table = Table(mut_rows, colWidths=[24, 40, 52, 55, 52, 54, 40, 75, 112])
    mut_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), primary_color),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ("PADDING", (0, 0), (-1, -1), 3),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7FAFC")]),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ]))
    story.append(mut_table)
    story.append(Spacer(1, 8))

    # Embed Pareto Landscape Figure
    pareto_fig_path = workspace_dir / "rosetta_learning" / "figures" / "rosetta_pareto_landscape.png"
    if pareto_fig_path.exists():
        img_pareto = Image(str(pareto_fig_path), width=6.8 * inch, height=4.4 * inch)
        story.append(KeepTogether([img_pareto, Spacer(1, 8)]))

    story.append(PageBreak())

    # =========================================================================
    # Section 4: Energy Decomposition & Experimental Translation
    # =========================================================================
    story.append(Paragraph("4. Physical Energy Decomposition & Experimental Translation", h1_style))
    story.append(Paragraph(
        "Energy term decomposition across prioritized candidates illustrates the exact physical drivers "
        "(Lennard-Jones attractive vs repulsive vdW, Lazaridis-Karplus solvation, and hydrogen-bonding networks) "
        "governing design fitness.",
        body_style
    ))

    decomp_fig_path = workspace_dir / "rosetta_learning" / "figures" / "rosetta_energy_decomposition.png"
    if decomp_fig_path.exists():
        img_decomp = Image(str(decomp_fig_path), width=6.8 * inch, height=3.6 * inch)
        story.append(KeepTogether([img_decomp, Spacer(1, 10)]))

    story.append(Paragraph("Experimental Validation Roadmap (Wet-Lab Translation)", h2_style))
    
    exp_steps = [
        "<b>1. Heterologous Expression & Purification:</b> Clone WT and mutant genes into <code>pET-28a(+)</code> (His6-TEV-HEWL) for expression in <i>Pichia pastoris</i> X-33 or <i>E. coli</i> BL21(DE3) with periplasmic targeting to guarantee formation of all 4 native disulfide bonds (Cys6-Cys127, Cys30-Cys115, Cys64-Cys80, Cys76-Cys94). Purify via SP-Sepharose cation exchange and SEC.",
        "<b>2. Thermal Stability & Fold Integrity (nanoDSF / CD):</b> Measure intrinsic tryptophan emission ratio (F350/F330) during thermal ramp (20°C to 95°C at 1°C/min) to determine melting temperatures (Tm) and folding enthalpies (ΔH_unf). Acceptance threshold: ΔTm ≥ -2.0°C vs WT.",
        "<b>3. Turbidimetric Clearance Assay:</b> Quantify bulk bactericidal activity against lyophilized <i>Micrococcus lysodeikticus</i> cells in 66 mM potassium phosphate buffer (pH 6.24, 25°C) at 450 nm.",
        "<b>4. Fluorogenic Subsite Kinetic Characterization:</b> Measure steady-state kinetics (k_cat, K_M, k_cat/K_M) using 4-Methylumbelliferyl-β-D-glycosides (4-MUG_n) to isolate subsite-specific cleavage efficiencies.",
    ]
    for step in exp_steps:
        story.append(Paragraph(step, body_style))
        story.append(Spacer(1, 3))

    doc.build(story, canvasmaker=NumberedCanvas)
    return output_pdf_path


if __name__ == "__main__":
    workspace = Path(__file__).resolve().parent.parent
    pdf_out = workspace / "HEWL_Biophysics_Enzyme_Design_Research_Report.pdf"
    build_pdf_report(workspace, pdf_out)
    print(f"Successfully generated research PDF report: {pdf_out}")
