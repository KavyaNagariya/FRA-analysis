import os
import io
import base64
import pytest
import pypdf
from PIL import Image as PILImage
import pandas as pd
import numpy as np

from src.report import generate_report
from src.plotter import generate_comparison_plot
from src.pipeline import run_pipeline

def create_dummy_base64_image():
    """Generates a simple dummy base64 PNG string."""
    buf = io.BytesIO()
    img = PILImage.new('RGB', (400, 200), color=(56, 189, 248))
    img.save(buf, format='PNG')
    b64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{b64}"

@pytest.fixture
def sample_analysis_result():
    return {
        "status": "Warning",
        "severity": "Medium",
        "fault_type": "Insulation Degradation",
        "correlation": 0.9412,
        "shift": 4.56,
        "confidence": 88.5,
        "composite_score": 79.4,
        "per_band": {
            "Low (Core)": {
                "range": "< 2 kHz",
                "ccf": 0.9950,
                "max_dev": 0.85,
                "status": "Healthy"
            },
            "Mid (Winding)": {
                "range": "2 - 100 kHz",
                "ccf": 0.9820,
                "max_dev": 1.20,
                "status": "Healthy"
            },
            "High (Insulation)": {
                "range": "> 100 kHz",
                "ccf": 0.8920,
                "max_dev": 4.56,
                "status": "Warning"
            }
        },
        "recommendation": "Schedule a DGA (Dissolved Gas Analysis) within 30 days to evaluate dielectric insulation condition.",
        "transformer_id": "TX-9001",
        "test_date": "2026-10-02"
    }

def test_generate_report_with_base64_bode_plot(tmp_path, sample_analysis_result):
    """Verifies that a base64-encoded Bode plot is decoded and embedded into the PDF."""
    pdf_path = str(tmp_path / "test_report_with_plot.pdf")
    b64_plot = create_dummy_base64_image()
    
    output_path = generate_report(sample_analysis_result, bode_plot=b64_plot, output_path=pdf_path)
    
    assert os.path.exists(output_path)
    assert os.path.getsize(output_path) > 0
    
    # Verify PDF structure using pypdf
    reader = pypdf.PdfReader(output_path)
    assert len(reader.pages) >= 1
    
    # Total images across all pages should be at least 1 (the embedded Bode plot)
    total_images = sum(len(page.images) for page in reader.pages)
    assert total_images >= 1

def test_generate_report_subband_table_and_health_score(tmp_path, sample_analysis_result):
    """Verifies that the PDF text contains the sub-band breakdown table and health integrity score."""
    pdf_path = str(tmp_path / "test_report_content.pdf")
    b64_plot = create_dummy_base64_image()
    
    generate_report(sample_analysis_result, bode_plot=b64_plot, output_path=pdf_path)
    
    reader = pypdf.PdfReader(pdf_path)
    all_text = " ".join(page.extract_text() for page in reader.pages)
    
    # Check Health Integrity Score
    assert "Health Integrity Score" in all_text
    assert "79.4" in all_text
    
    # Check Sub-band Diagnostic Breakdown
    assert "Sub-band" in all_text or "Sub-Band" in all_text
    assert "Low (Core)" in all_text
    assert "Mid (Winding)" in all_text
    assert "High (Insulation)" in all_text
    assert "0.9950" in all_text
    assert "4.56" in all_text
    
    # Check Actionable Recommendations
    assert "Recommendation" in all_text
    assert "Dissolved Gas Analysis" in all_text

def test_generate_report_handles_insufficient_data(tmp_path):
    """Verifies handling of bands with Insufficient Data without errors."""
    pdf_path = str(tmp_path / "test_insufficient.pdf")
    result = {
        "status": "Insufficient Data",
        "severity": "Unknown",
        "fault_type": "Analysis Pending",
        "correlation": 0.0,
        "shift": 0.0,
        "confidence": 0.0,
        "composite_score": 0.0,
        "per_band": {
            "Low (Core)": {
                "range": "< 2 kHz",
                "ccf": None,
                "max_dev": None,
                "status": "Insufficient Data"
            },
            "Mid (Winding)": {
                "range": "2 - 100 kHz",
                "ccf": None,
                "max_dev": None,
                "status": "Insufficient Data"
            },
            "High (Insulation)": {
                "range": "> 100 kHz",
                "ccf": None,
                "max_dev": None,
                "status": "Insufficient Data"
            }
        },
        "recommendation": "Insufficient data points across all bands. Please perform a higher-resolution sweep.",
        "transformer_id": "TX-INSUFF"
    }
    
    output_path = generate_report(result, output_path=pdf_path)
    assert os.path.exists(output_path)
    
    reader = pypdf.PdfReader(output_path)
    all_text = " ".join(page.extract_text() for page in reader.pages)
    assert "Insufficient Data" in all_text
    assert "Health Integrity Score" in all_text

def test_pipeline_integration_with_report(tmp_path):
    """E2E test: run_pipeline -> generate_comparison_plot -> generate_report."""
    results = run_pipeline("data/raw/fra_healthy.csv")
    result = results[0]
    
    # Check that bode_plot is attached or can be plotted
    assert "frequencies" in result
    assert "magnitude_healthy" in result
    assert "magnitude_uploaded" in result
    
    pdf_path = str(tmp_path / "e2e_pipeline_report.pdf")
    bode_plot = result.get("bode_plot")
    output_path = generate_report(result, bode_plot=bode_plot, output_path=pdf_path)
    
    assert os.path.exists(output_path)
    reader = pypdf.PdfReader(output_path)
    all_text = " ".join(page.extract_text() for page in reader.pages)
    
    assert "Health Integrity Score" in all_text
    assert "Sub-band" in all_text or "Sub-Band" in all_text
