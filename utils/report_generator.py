# =============================================================================
# utils/report_generator.py — PDF Report Generator (ReportLab)
# =============================================================================
import io
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer,
                                 Table, TableStyle, HRFlowable)
from reportlab.lib.enums import TA_CENTER, TA_LEFT


INDIGO = colors.HexColor("#6366F1")
DARK   = colors.HexColor("#111827")
GRAY   = colors.HexColor("#6B7280")
GREEN  = colors.HexColor("#16A34A")
RED    = colors.HexColor("#DC2626")
LIGHT  = colors.HexColor("#F9FAFB")


def generate_pdf_report(parsed: dict, result: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        leftMargin=20*mm, rightMargin=20*mm,
        topMargin=18*mm, bottomMargin=18*mm,
    )

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle("title", fontSize=22, textColor=DARK,
                                  fontName="Helvetica-Bold", spaceAfter=4)
    sub_style   = ParagraphStyle("sub",   fontSize=11, textColor=GRAY,
                                  fontName="Helvetica", spaceAfter=16)
    h2_style    = ParagraphStyle("h2",    fontSize=13, textColor=INDIGO,
                                  fontName="Helvetica-Bold", spaceAfter=6, spaceBefore=14)
    body_style  = ParagraphStyle("body",  fontSize=10, textColor=DARK,
                                  fontName="Helvetica", spaceAfter=4, leading=15)
    small_style = ParagraphStyle("small", fontSize=9, textColor=GRAY,
                                  fontName="Helvetica", spaceAfter=3)

    story = []

    # ── Header ────────────────────────────────────────────────────────────────
    story.append(Paragraph("ResumeAI — Analysis Report", title_style))
    story.append(Paragraph(
        f"Generated on {datetime.now().strftime('%d %B %Y, %I:%M %p')}",
        sub_style
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=INDIGO))
    story.append(Spacer(1, 10))

    # ── Candidate Info ────────────────────────────────────────────────────────
    story.append(Paragraph("Candidate Information", h2_style))
    info_data = [
        ["Name",     parsed.get("name", "—")],
        ["Email",    parsed.get("email", "—")],
        ["Phone",    parsed.get("phone", "—")],
        ["LinkedIn", parsed.get("linkedin", "—")],
        ["GitHub",   parsed.get("github", "—")],
        ["File",     parsed.get("filename", "—")],
    ]
    info_table = Table(info_data, colWidths=[40*mm, 130*mm])
    info_table.setStyle(TableStyle([
        ("FONTNAME",  (0,0),(-1,-1), "Helvetica"),
        ("FONTSIZE",  (0,0),(-1,-1), 10),
        ("FONTNAME",  (0,0),(0,-1),  "Helvetica-Bold"),
        ("TEXTCOLOR", (0,0),(0,-1),  INDIGO),
        ("TEXTCOLOR", (1,0),(1,-1),  DARK),
        ("ROWBACKGROUNDS", (0,0),(-1,-1), [colors.white, LIGHT]),
        ("ROWPADDING", (0,0),(-1,-1), 5),
        ("GRID", (0,0),(-1,-1), 0.3, colors.HexColor("#E5E7EB")),
        ("ROUNDEDCORNERS", [4]),
    ]))
    story.append(info_table)
    story.append(Spacer(1, 10))

    # ── Scores ────────────────────────────────────────────────────────────────
    story.append(Paragraph("ATS Scores", h2_style))
    score_data = [
        ["Metric", "Score", "Status"],
        ["ATS Match Score",  f"{result['ats_score']}%",   result['label']],
        ["Resume Quality",   f"{result['quality_score']}%", "Good" if result['quality_score'] >= 60 else "Needs Work"],
        ["Keyword Match",    f"{result['keyword_match_pct']}%", "—"],
        ["Skills Matched",   str(len(result['matched_skills'])), "—"],
    ]
    score_table = Table(score_data, colWidths=[70*mm, 40*mm, 60*mm])
    score_table.setStyle(TableStyle([
        ("BACKGROUND",  (0,0),(-1,0),  INDIGO),
        ("TEXTCOLOR",   (0,0),(-1,0),  colors.white),
        ("FONTNAME",    (0,0),(-1,0),  "Helvetica-Bold"),
        ("FONTSIZE",    (0,0),(-1,-1), 10),
        ("FONTNAME",    (0,1),(-1,-1), "Helvetica"),
        ("TEXTCOLOR",   (0,1),(-1,-1), DARK),
        ("ROWBACKGROUNDS", (0,1),(-1,-1), [colors.white, LIGHT]),
        ("ROWPADDING",  (0,0),(-1,-1), 6),
        ("GRID",        (0,0),(-1,-1), 0.3, colors.HexColor("#E5E7EB")),
        ("ALIGN",       (1,0),(-1,-1), "CENTER"),
    ]))
    story.append(score_table)
    story.append(Spacer(1, 10))

    # ── Matched Skills ────────────────────────────────────────────────────────
    story.append(Paragraph("Matched Skills", h2_style))
    if result["matched_skills"]:
        story.append(Paragraph(", ".join(result["matched_skills"]), body_style))
    else:
        story.append(Paragraph("No overlapping skills found.", small_style))

    # ── Missing Skills ────────────────────────────────────────────────────────
    story.append(Paragraph("Missing Skills (from Job Description)", h2_style))
    if result["missing_skills"]:
        story.append(Paragraph(", ".join(result["missing_skills"]), body_style))
    else:
        story.append(Paragraph("No missing skills — great coverage!", small_style))

    # ── Suggestions ───────────────────────────────────────────────────────────
    story.append(Paragraph("Improvement Suggestions", h2_style))
    for i, tip in enumerate(result.get("suggestions", []), 1):
        story.append(Paragraph(f"{i}. {tip}", body_style))

    # ── Suggested Roles ───────────────────────────────────────────────────────
    story.append(Paragraph("Suggested Job Roles", h2_style))
    roles = result.get("suggested_roles", [])
    if roles:
        role_data = [["Job Role", "Match %"]] + [[r, f"{p}%"] for r, p in roles]
        role_table = Table(role_data, colWidths=[110*mm, 40*mm])
        role_table.setStyle(TableStyle([
            ("BACKGROUND",  (0,0),(-1,0), INDIGO),
            ("TEXTCOLOR",   (0,0),(-1,0), colors.white),
            ("FONTNAME",    (0,0),(-1,0), "Helvetica-Bold"),
            ("FONTSIZE",    (0,0),(-1,-1), 10),
            ("FONTNAME",    (0,1),(-1,-1), "Helvetica"),
            ("TEXTCOLOR",   (0,1),(-1,-1), DARK),
            ("ROWBACKGROUNDS", (0,1),(-1,-1), [colors.white, LIGHT]),
            ("ROWPADDING",  (0,0),(-1,-1), 6),
            ("GRID",        (0,0),(-1,-1), 0.3, colors.HexColor("#E5E7EB")),
            ("ALIGN",       (1,0),(1,-1), "CENTER"),
        ]))
        story.append(role_table)
    else:
        story.append(Paragraph("No role predictions available.", small_style))

    # ── Footer ────────────────────────────────────────────────────────────────
    story.append(Spacer(1, 16))
    story.append(HRFlowable(width="100%", thickness=0.5, color=GRAY))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Generated by ResumeAI · Final Year B.Tech CSE Project · AI & ML",
        ParagraphStyle("footer", fontSize=8, textColor=GRAY,
                       fontName="Helvetica", alignment=TA_CENTER)
    ))

    doc.build(story)
    return buffer.getvalue()
