import os
import io
import base64
from datetime import datetime
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle,
    Image,
    KeepTogether,
    HRFlowable
)


STATUS_PALETTE = {
    "healthy": colors.HexColor("#15803d"),
    "warning": colors.HexColor("#b45309"),
    "danger": colors.HexColor("#b91c1c"),
    "critical": colors.HexColor("#b91c1c"),
    "insufficient": colors.HexColor("#64748b")
}
DEFAULT_STATUS_COLOR = colors.HexColor("#64748b")

STATUS_PROTOCOLS = {
    "critical": (
        "<b>Mandatory Protocol:</b> Significant frequency response deviations detected. "
        "Immediately de-energize asset if in service. Perform winding resistance, excitation current, "
        "and dissolved gas analysis (DGA). Schedule internal tank inspection to confirm mechanical winding/core displacement."
    ),
    "danger": (
        "<b>Mandatory Protocol:</b> Significant frequency response deviations detected. "
        "Immediately de-energize asset if in service. Perform winding resistance, excitation current, "
        "and dissolved gas analysis (DGA). Schedule internal tank inspection to confirm mechanical winding/core displacement."
    ),
    "warning": (
        "<b>Targeted Protocol:</b> Moderate deviations observed in frequency response signature. "
        "Schedule oil sampling for Dissolved Gas Analysis (DGA) within 30 days. Re-sweep SFRA at next "
        "scheduled maintenance outage to monitor fault progression."
    ),
    "insufficient": (
        "<b>Targeted Protocol:</b> Less than 10 valid data points detected in one or more IEEE sub-bands. "
        "Sweep does not meet IEEE C57.149 minimum resolution. Re-acquire SFRA sweep from 20 Hz to 1 MHz."
    ),
    "healthy": (
        "<b>Targeted Protocol:</b> Frequency response aligns with healthy baseline across all IEEE sub-bands. "
        "No mechanical deformation or dielectric degradation indicated. Continue standard maintenance interval."
    )
}


def _status_color(st):
    st_clean = str(st).strip().lower()
    for key, color in STATUS_PALETTE.items():
        if key in st_clean:
            return color
    return DEFAULT_STATUS_COLOR


def _decode_bode_plot(bode_plot):
    """
    Decodes a base64 encoded image string or buffer into an io.BytesIO stream.
    Supports both raw base64 and data URI schemes (data:image/png;base64,...).
    """
    if not bode_plot:
        return None
    try:
        if isinstance(bode_plot, str):
            if "," in bode_plot:
                bode_plot = bode_plot.split(",", 1)[1]
            img_bytes = base64.b64decode(bode_plot.strip())
        elif isinstance(bode_plot, (bytes, bytearray)):
            img_bytes = bytes(bode_plot)
        elif hasattr(bode_plot, "read"):
            img_bytes = bode_plot.read()
        else:
            return None
        buf = io.BytesIO(img_bytes)
        buf.seek(0)
        return buf
    except Exception as e:
        print(f"Error decoding Bode plot image: {e}")
        return None


def _extract_band_info(per_band, match_tokens, default_name, default_range):
    """
    Extracts metrics for a specific sub-band from per_band dictionary
    supporting multiple key naming conventions.
    """
    found = None
    for k, v in per_band.items():
        k_lower = str(k).lower()
        if any(token.lower() in k_lower for token in match_tokens):
            found = v
            break
            
    if found is None:
        return {
            "name": default_name,
            "range": default_range,
            "ccf": None,
            "max_dev": None,
            "status": "Not Evaluated"
        }

    return {
        "name": default_name,
        "range": found.get("range", default_range),
        "ccf": found.get("ccf") if found.get("ccf") is not None else found.get("CCF"),
        "max_dev": found.get("max_dev") if found.get("max_dev") is not None else found.get("MaxDev_dB"),
        "status": found.get("status", "N/A")
    }


def generate_report(result, bode_plot=None, output_path=None):
    """
    Generates an enriched, IEEE C57.149 compliant diagnostic PDF report.
    
    Parameters:
    - result (dict): Diagnostic dictionary from advanced_analysis or run_pipeline.
    - bode_plot (str, optional): Base64 encoded Bode plot string or data URI.
    - output_path (str, optional): Output PDF file path. Defaults to 'reports/report.pdf'.
    
    Returns:
    - str: Absolute or relative path to the generated PDF report.
    """
    if output_path is None:
        output_path = os.path.join("reports", "report.pdf")
        
    out_dir = os.path.dirname(output_path)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)

    # Resolve Bode plot from argument or result
    if bode_plot is None:
        bode_plot = result.get("bode_plot")
        
    # Auto-generate plot if raw frequency and magnitudes are available but no plot string was passed
    chart_data = result.get("chart_data", {}) if isinstance(result.get("chart_data"), dict) else {}
    freqs = result.get("frequencies") or chart_data.get("frequencies")
    mag_h = result.get("magnitude_healthy") or chart_data.get("magnitude_healthy")
    mag_u = result.get("magnitude_uploaded") or chart_data.get("magnitude_uploaded")

    if bode_plot is None and freqs and mag_h and mag_u:
        try:
            from src.plotter import generate_comparison_plot
            df_ref = pd.DataFrame({"Frequency": freqs, "Magnitude": mag_h})
            df_test = pd.DataFrame({"Frequency": freqs, "Magnitude": mag_u})
            bode_plot = generate_comparison_plot(df_ref, df_test, theme='light')
        except Exception as e:
            print(f"Auto Bode plot generation warning: {e}")

    # Document Setup (Letter, 36pt margins for clean layout)
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom Typography & Styling
    brand_blue = colors.HexColor("#0284c7")
    slate_900 = colors.HexColor("#0f172a")
    slate_700 = colors.HexColor("#334155")
    slate_100 = colors.HexColor("#f1f5f9")
    border_slate = colors.HexColor("#cbd5e1")
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        fontName='Helvetica-Bold',
        textColor=slate_900,
        spaceAfter=4
    )
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=slate_700,
        spaceAfter=10
    )
    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontSize=13,
        leading=17,
        fontName='Helvetica-Bold',
        textColor=brand_blue,
        spaceBefore=10,
        spaceAfter=6
    )
    score_title_style = ParagraphStyle(
        'ScoreTitle',
        parent=styles['Normal'],
        fontSize=11,
        fontName='Helvetica-Bold',
        textColor=slate_900,
        leading=14
    )
    score_val_style = ParagraphStyle(
        'ScoreValue',
        parent=styles['Normal'],
        fontSize=24,
        leading=28,
        fontName='Helvetica-Bold',
        textColor=brand_blue,
        alignment=1 # Center
    )
    cell_bold = ParagraphStyle(
        'CellBold',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        fontName='Helvetica-Bold',
        textColor=slate_900
    )
    cell_normal = ParagraphStyle(
        'CellNormal',
        parent=styles['Normal'],
        fontSize=9,
        leading=11,
        textColor=slate_700
    )
    rec_style = ParagraphStyle(
        'RecText',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        textColor=slate_900
    )
    footer_style = ParagraphStyle(
        'FooterNote',
        parent=styles['Normal'],
        fontSize=8,
        leading=10,
        textColor=colors.HexColor("#64748b")
    )

    content = []

    # 1. Header Section
    content.append(Paragraph("FRA Diagnostic Analysis Report", title_style))
    content.append(Paragraph(
        "<b>Standard:</b> IEEE C57.149-2012 / IEC 60076-18 Standards-Aligned SFRA Diagnostic Pipeline | "
        "<b>System:</b> AI-Powered Hybrid Transformer Integrity Monitor",
        subtitle_style
    ))
    content.append(HRFlowable(width="100%", thickness=1.5, color=brand_blue, spaceBefore=0, spaceAfter=8))

    # Support both flat and nested diagnostic dictionaries
    diag = result.get("diagnosis", {}) if isinstance(result.get("diagnosis"), dict) else {}
    per_band_dict = result.get("per_band") or diag.get("per_band") or {}

    # Metadata & Asset Info
    transformer_id = result.get("transformer_id") or result.get("asset_id") or diag.get("transformer_id") or "TX-ASSET-01"
    test_date = result.get("test_date") or result.get("date") or diag.get("test_date") or datetime.now().strftime("%Y-%m-%d %H:%M")
    winding_type = result.get("winding_type") or diag.get("winding_type") or "HV to LV Transfer Function"
    overall_status = result.get("status") or diag.get("status") or "N/A"
    severity = result.get("severity") or diag.get("severity") or "N/A"

    meta_data = [
        [
            Paragraph(f"<b>Asset / Transformer ID:</b> {transformer_id}", cell_normal),
            Paragraph(f"<b>Inspection Date:</b> {test_date}", cell_normal)
        ],
        [
            Paragraph(f"<b>Winding Configuration:</b> {winding_type}", cell_normal),
            Paragraph(f"<b>Overall Status / Severity:</b> <b>{overall_status}</b> ({severity})", cell_normal)
        ]
    ]
    meta_table = Table(meta_data, colWidths=[270, 270])
    meta_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), slate_100),
        ('BOX', (0, 0), (-1, -1), 0.5, border_slate),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#e2e8f0")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    content.append(meta_table)
    content.append(Spacer(1, 8))

    # 2. Executive Summary & Prominent Health Integrity Score
    composite_score = float(result.get("composite_score") if result.get("composite_score") is not None else diag.get("composite_score", 0.0))
    fault_type = result.get("fault_type") or diag.get("fault_type") or "N/A"
    confidence = float(result.get("confidence") if result.get("confidence") is not None else diag.get("confidence", 0.0))
    corr = float(result.get("correlation") if result.get("correlation") is not None else diag.get("correlation", 0.0))
    shift = float(result.get("shift") if result.get("shift") is not None else (diag.get("shift") or diag.get("max_dev") or 0.0))

    # Color badge based on composite health score
    if composite_score >= 85:
        score_color = colors.HexColor("#16a34a") # Green
        health_verdict = "Optimal Asset Health"
    elif composite_score >= 70:
        score_color = colors.HexColor("#d97706") # Amber
        health_verdict = "Moderate Degradation Detected"
    elif composite_score >= 50:
        score_color = colors.HexColor("#ea580c") # Orange
        health_verdict = "Severe Deviation / Alert"
    else:
        score_color = colors.HexColor("#dc2626") # Red
        health_verdict = "Critical Fault Condition"

    score_val_styled = ParagraphStyle(
        'ScoreValColor',
        parent=score_val_style,
        textColor=score_color
    )

    kpi_data = [
        [
            Paragraph("<b>Overall Health Integrity Score</b><br/><font size=8 color='#64748b'>Blended Physics (60%) + ML (40%)</font>", score_title_style),
            Paragraph(f"<b>{composite_score:.1f}%</b>", score_val_styled),
            Paragraph(
                f"<b>Condition Assessment:</b> {health_verdict}<br/>"
                f"<b>AI Fault Signature:</b> {fault_type} ({confidence:.1f}% conf.)<br/>"
                f"<b>Overall Correlation (CCF):</b> {corr:.4f} | <b>Max Dev:</b> {shift:.2f} dB",
                cell_normal
            )
        ]
    ]
    kpi_table = Table(kpi_data, colWidths=[170, 110, 260])
    kpi_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, score_color),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, border_slate),
    ]))
    content.append(kpi_table)
    content.append(Spacer(1, 8))

    # 3. Sub-band Diagnostic Breakdown Table (IEEE C57.149)
    content.append(Paragraph("Sub-band Diagnostic Breakdown (IEEE C57.149 Standards Table)", section_heading))
    
    per_band_dict = result.get("per_band", {})
    band_low = _extract_band_info(per_band_dict, ["low", "core", "lf"], "Low (Core)", "< 2 kHz")
    band_mid = _extract_band_info(per_band_dict, ["mid", "winding", "mf"], "Mid (Winding)", "2 - 100 kHz")
    band_high = _extract_band_info(per_band_dict, ["high", "insulation", "hf"], "High (Insulation)", "> 100 kHz")

    def _fmt_ccf(val):
        return f"{val:.4f}" if val is not None else "N/A"

    def _fmt_dev(val):
        return f"{val:.2f} dB" if val is not None else "N/A"


    subband_table_data = [
        [
            Paragraph("<b>Sub-band / Component</b>", cell_bold),
            Paragraph("<b>Frequency Range</b>", cell_bold),
            Paragraph("<b>CCF (Correlation)</b>", cell_bold),
            Paragraph("<b>Max Deviation</b>", cell_bold),
            Paragraph("<b>Diagnostic Status</b>", cell_bold)
        ]
    ]

    for band in [band_low, band_mid, band_high]:
        st = band["status"]
        st_color = _status_color(st)
        status_para = Paragraph(f"<font color='{st_color.hexval()}'><b>{st}</b></font>", cell_bold)
        subband_table_data.append([
            Paragraph(band["name"], cell_normal),
            Paragraph(band["range"], cell_normal),
            Paragraph(_fmt_ccf(band["ccf"]), cell_normal),
            Paragraph(_fmt_dev(band["max_dev"]), cell_normal),
            status_para
        ])

    subband_table = Table(subband_table_data, colWidths=[120, 95, 110, 105, 110])
    subband_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), slate_900),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, border_slate),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, slate_100]),
        ('TOPPADDING', (0, 0), (-1, -1), 5),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 5),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    content.append(subband_table)
    content.append(Spacer(1, 8))

    # 4. Bode Comparison Plot
    content.append(Paragraph("Frequency Response Bode Plot Comparison", section_heading))
    img_buf = _decode_bode_plot(bode_plot)
    if img_buf is not None:
        try:
            # Printable width is 540 pt; 500 pt width by 190 pt height fits cleanly
            plot_img = Image(img_buf, width=500, height=190)
            content.append(plot_img)
        except Exception as e:
            content.append(Paragraph(f"<i>Could not render Bode plot: {e}</i>", cell_normal))
    else:
        content.append(Paragraph(
            "<i>Bode plot data was not provided for this inspection sweep.</i>", cell_normal
        ))
    content.append(Spacer(1, 8))

    # 5. Actionable Recommendations Section
    content.append(Paragraph("Actionable Recommendations & Maintenance Guidance", section_heading))
    primary_rec = result.get("recommendation", "Continue routine monitoring as per standard schedule.")
    
    rec_flowables = [
        Paragraph(f"<b>Primary Assessment:</b> {primary_rec}", rec_style),
        Spacer(1, 4)
    ]
    
    # Specific targeted guidance based on worst band or overall status
    st_lower = overall_status.lower()
    action_note = STATUS_PROTOCOLS["healthy"]
    for k in ["critical", "danger", "warning", "insufficient"]:
        if k in st_lower:
            action_note = STATUS_PROTOCOLS[k]
            break

    rec_flowables.append(Paragraph(action_note, cell_normal))
    rec_flowables.append(Spacer(1, 6))

    # Context-aware component-level breakdown
    def _band_guidance(comp_name, band_info):
        st = str(band_info.get("status", "")).lower()
        if "critical" in st or "danger" in st:
            if "core" in comp_name.lower():
                return "Severe deviation detected. Magnetic core deformation or core ground fault suspected. Check core ground current and excitation current."
            elif "winding" in comp_name.lower():
                return "Severe deviation detected. Radial or axial mechanical winding deformation indicated. Perform DC winding resistance and leakage reactance tests."
            else:
                return "Severe deviation detected. Dielectric degradation or main lead displacement indicated. Perform insulation resistance and bushing inspections."
        elif "warning" in st:
            if "core" in comp_name.lower():
                return "Moderate deviation. Inspect magnetic circuit grounding and monitor no-load losses."
            elif "winding" in comp_name.lower():
                return "Moderate deviation. Review short-circuit event history and re-sweep SFRA at next scheduled outage."
            else:
                return "Moderate deviation. Schedule oil sampling for Dissolved Gas Analysis (DGA) within 30 days."
        elif "insufficient" in st:
            return "Insufficient data points (< 10 points) in this sub-band. Re-sweep frequency response."
        else:
            return "Operating within IEEE C57.149 normal parameters. No physical deformation indicated."

    rec_flowables.append(Paragraph("<b>Component-Level Guidance (IEEE C57.149):</b>", cell_bold))
    rec_flowables.append(Paragraph(f"• <b>Core (Low Band, &lt; 2 kHz):</b> {_band_guidance('Core', band_low)}", cell_normal))
    rec_flowables.append(Paragraph(f"• <b>Winding (Mid Band, 2–100 kHz):</b> {_band_guidance('Winding', band_mid)}", cell_normal))
    rec_flowables.append(Paragraph(f"• <b>Insulation (High Band, &gt; 100 kHz):</b> {_band_guidance('Insulation', band_high)}", cell_normal))

    rec_box = Table([[rec_flowables]], colWidths=[540])
    rec_box.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#0284c7")),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
        ('RIGHTPADDING', (0, 0), (-1, -1), 8),
    ]))
    content.append(rec_box)
    content.append(Spacer(1, 8))

    # 6. Compliance Footer Note
    footer_note = (
        "<b>Deterministic Physics Floor:</b> As mandated by IEEE C57.149-2012 and IEC 60076-18, the diagnostic status is "
        "governed strictly by the worst-performing sub-band (Low: Core, Mid: Winding, High: Insulation). "
        "Machine Learning predictions provide fault signature classification and escalation without overriding physical limits."
    )
    content.append(Paragraph(footer_note, footer_style))

    # Build the PDF document
    doc.build(content)

    return output_path