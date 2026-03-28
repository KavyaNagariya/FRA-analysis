import os
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def generate_report(result):
    os.makedirs("reports", exist_ok=True)
    file_path = os.path.join("reports", "report.pdf")

    # Initialize document
    doc = SimpleDocTemplate(file_path, pagesize=letter)
    styles = getSampleStyleSheet()
    
    # Custom Styles
    title_style = ParagraphStyle(
        'TitleStyle',
        parent=styles['Heading1'],
        fontSize=18,
        textColor=colors.HexColor("#0ea5e9"),
        spaceAfter=20
    )
    
    content = []

    # 1. Header Section
    content.append(Paragraph("FRA Diagnostic Analysis Report", title_style))
    content.append(Paragraph("System: AI-Powered Transformer Monitor", styles['Normal']))
    content.append(Spacer(1, 12))
    content.append(Paragraph("-" * 80, styles['Normal']))
    content.append(Spacer(1, 12))

    # 2. Key Metrics Table (REPLACE YOUR OLD TABLE SECTION WITH THIS)
    data = [
        ["Parameter", "Value"],
        ["Status", str(result.get('status', 'N/A'))],
        ["Fault Type", str(result.get('fault_type', 'N/A'))],
        ["Severity", str(result.get('severity', 'N/A'))],
        ["Correlation Index", f"{result.get('correlation', 0):.4f}"],
        ["Max Deviation", f"{result.get('shift', 0):.2f} dB"],
        ["AI Confidence", f"{result.get('confidence', 0)}%"]
    ]

    # Create the table object first
    table = Table(data, colWidths=[150, 250])

    # Now apply the styling to the table object
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#1e293b")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    
    # Finally, add the table to the document content list
    content.append(table)
    content.append(Spacer(1, 20))

    # 3. Recommendation Section
    content.append(Paragraph("<b>Expert Recommendation:</b>", styles['Heading3']))
    rec_text = result.get('recommendation', "Manual inspection advised.")
    content.append(Paragraph(rec_text, styles['Normal']))

    # Build the actual PDF file
    doc.build(content)
    
    return file_path