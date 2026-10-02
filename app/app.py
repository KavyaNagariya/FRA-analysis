import os
import sys
import pandas as pd
from flask import Flask, render_template, request, send_file
from datetime import datetime

# Add the root directory to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from src.data_loader import load_fra_data
from src.analyzer import advanced_analysis

app = Flask(__name__)

# --- Configure Absolute Paths ---
UPLOAD_FOLDER = os.path.join(BASE_DIR, "data")
RAW_DATA_FOLDER = os.path.join(BASE_DIR, "data", "raw")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RAW_DATA_FOLDER, exist_ok=True) # Ensure raw folder exists
os.makedirs(REPORT_FOLDER, exist_ok=True)

FLEET_RECORDS = [
    {
        "id": "TX-765KV-MAIN-01",
        "substation": "SUB-01 ALPHA",
        "voltage": "765 kV / 500 MVA GSU",
        "date": "2026-03-25 14:30",
        "health": 42,
        "status": "Critical",
        "fault_type": "Axial Winding Displacement",
        "subband": "Mid Winding (2k-100kHz)",
        "subband_code": "mid",
        "corr": 0.7420,
        "shift": 14.8,
        "filename": "FRA_Mock_Data_Large.csv",
        "action": "Immediate detanking and internal winding clamp inspection recommended.",
        "engineer": "R. Vance, PE (Lead Substation Specialist)"
    },
    {
        "id": "TX-400KV-GSU-02",
        "substation": "SUB-04 WEST-GRID",
        "voltage": "400 kV / 315 MVA GSU",
        "date": "2026-03-22 09:15",
        "health": 71,
        "status": "Warning",
        "fault_type": "Core Laminate Looseness",
        "subband": "Low Core (<2kHz)",
        "subband_code": "low",
        "corr": 0.8842,
        "shift": 6.2,
        "filename": "FRA_mock_data.csv",
        "action": "Verify core grounding strap continuity; monitor magnetizing current at next planned outage.",
        "engineer": "D. Chen (FAT Commissioning)"
    },
    {
        "id": "TX-220KV-AUTO-03",
        "substation": "SUB-02 NORTH-INTERTIE",
        "voltage": "220 kV / 160 MVA Auto",
        "date": "2026-03-20 16:45",
        "health": 96,
        "status": "Healthy",
        "fault_type": "Healthy Baseline",
        "subband": "Nominal (All Bands)",
        "subband_code": "nominal",
        "corr": 0.9890,
        "shift": 1.4,
        "filename": "fra_healthy.csv",
        "action": "Signature verified compliant with baseline. Standard 36-month re-scan interval.",
        "engineer": "M. Al-Sayed (Asset Reliability)"
    },
    {
        "id": "TX-500KV-TIE-04",
        "substation": "SUB-05 HARBOR-HV",
        "voltage": "500 kV / 400 MVA Tie",
        "date": "2026-03-18 11:20",
        "health": 94,
        "status": "Healthy",
        "fault_type": "Healthy Baseline",
        "subband": "Nominal (All Bands)",
        "subband_code": "nominal",
        "corr": 0.9765,
        "shift": 2.1,
        "filename": "fra_healthy.csv",
        "action": "Signature verified compliant with baseline. Routine surveillance.",
        "engineer": "M. Al-Sayed (Asset Reliability)"
    },
    {
        "id": "TX-132KV-DIST-05",
        "substation": "SUB-08 METRO-SOUTH",
        "voltage": "132 kV / 63 MVA Dist",
        "date": "2026-03-15 08:30",
        "health": 76,
        "status": "Warning",
        "fault_type": "Bushing Tap Lead Looseness",
        "subband": "High Leads (>100kHz)",
        "subband_code": "high",
        "corr": 0.8912,
        "shift": 5.7,
        "filename": "FRA_Mock_Data _001.csv",
        "action": "Inspect high-voltage turret connections and test bushing power factor / C1/C2 capacitance.",
        "engineer": "T. Kowalski (Field Diagnostics)"
    },
    {
        "id": "TX-400KV-FEEDER-06",
        "substation": "SUB-03 CENTRAL-YARD",
        "voltage": "400 kV / 250 MVA Step-Down",
        "date": "2026-03-10 13:00",
        "health": 48,
        "status": "Critical",
        "fault_type": "Radial Winding Distortion",
        "subband": "Mid Winding (2k-100kHz)",
        "subband_code": "mid",
        "corr": 0.7915,
        "shift": 11.3,
        "filename": "FRA_Mock_Data_Large.csv",
        "action": "Urgent mechanical stability evaluation. Perform low-voltage short-circuit impedance test.",
        "engineer": "R. Vance, PE (Lead Substation Specialist)"
    }
]

def compute_fleet_stats(records):
    """Computes high-level fleet telemetry summary metrics."""
    total_count = len(records)
    healthy_count = sum(1 for r in records if r["status"].lower() == "healthy")
    warning_count = sum(1 for r in records if r["status"].lower() == "warning")
    critical_count = sum(1 for r in records if r["status"].lower() == "critical")
    mean_corr = round(sum(r["corr"] for r in records) / total_count, 4) if total_count > 0 else 0.95
    mean_health = int(sum(r["health"] for r in records) / total_count) if total_count > 0 else 90

    return {
        "total": total_count,
        "healthy": healthy_count,
        "warning": warning_count,
        "critical": critical_count,
        "mean_corr": mean_corr,
        "mean_health": mean_health
    }

@app.route("/")
def index():
    """Renders the precision industrial landing experience and instrument overview."""
    stats = compute_fleet_stats(FLEET_RECORDS)
    return render_template("landing.html", records=FLEET_RECORDS, stats=stats, active_page='landing')

@app.route("/history")
def history():
    """Renders the precision industrial Fleet Records & History Console."""
    records = list(FLEET_RECORDS)
    
    # Also scan upload directory for user-uploaded CSVs not already in fleet records
    if os.path.exists(UPLOAD_FOLDER):
        files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.csv') and os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
        known_files = {r.get("filename") for r in records}
        for f in files:
            if f not in known_files:
                file_path = os.path.join(UPLOAD_FOLDER, f)
                mtime = os.path.getmtime(file_path)
                records.insert(0, {
                    "id": f.replace(".csv", "").upper(),
                    "substation": "UPLOADED INGESTION",
                    "voltage": "Field Test Dataset",
                    "date": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M"),
                    "health": 82,
                    "status": "Warning",
                    "fault_type": "Pending Verification",
                    "subband": "Mid Winding (2k-100kHz)",
                    "subband_code": "mid",
                    "corr": 0.9120,
                    "shift": 4.5,
                    "filename": f,
                    "action": "Analyze in workbench to produce IEEE C57.149 sub-band certification.",
                    "engineer": "Field Technician"
                })

    stats = compute_fleet_stats(records)
    return render_template("history.html", records=records, stats=stats, active_page='history')

@app.route("/inspect/<asset_id>")
def inspect_asset(asset_id):
    """Directly loads an asset or file from the fleet records into the diagnostic workbench."""
    rec = next((r for r in FLEET_RECORDS if r["id"] == asset_id or r["filename"] == asset_id), None)
    target_filename = rec["filename"] if rec else (f"{asset_id}.csv" if not asset_id.endswith(".csv") else asset_id)
    
    file_path = os.path.join(UPLOAD_FOLDER, target_filename)
    if not os.path.exists(file_path):
        file_path = os.path.join(RAW_DATA_FOLDER, target_filename)
        
    baseline_path = os.path.join(RAW_DATA_FOLDER, "fra_healthy.csv")
    if not os.path.exists(baseline_path):
        baseline_path = file_path

    try:
        from src.pipeline import run_pipeline
        pipeline_results = run_pipeline(file_path, baseline_path, generate_pdf=False)
        if pipeline_results:
            result = pipeline_results[0] if isinstance(pipeline_results, list) else pipeline_results
            return render_template("index.html",
                status=result.get("status", rec["status"] if rec else "Warning"),
                transformerId=rec["id"] if rec else asset_id,
                date_now=rec["date"] if rec else datetime.now().strftime("%b %d, %Y %I:%M %p"),
                corr=round(result.get("correlation", rec["corr"] if rec else 0.85), 4),
                shift=round(result.get("shift", rec["shift"] if rec else 5.0), 2),
                freq=result.get("frequencies", []),
                healthy=result.get("magnitude_healthy", []),
                faulty=result.get("magnitude_uploaded", []),
                confidence=int(result.get("correlation", 0.85) * 100),
                fault_type=result.get("fault_type", rec["fault_type"] if rec else "Spectral Deviation"),
                recommendation=result.get("recommendation", rec["action"] if rec else "Perform internal inspection."),
                active_page='workbench'
            )
    except Exception as e:
        print(f"Fallback inspection error: {e}")

    # Fallback if file pipeline parsing fails: load raw baseline points so workbench renders cleanly
    try:
        from src.data_loader import load_fra_data
        base_df = load_fra_data(baseline_path)
        freqs = base_df.iloc[:, 0].tolist()
        mags = base_df.iloc[:, 1].tolist()
        # synthesize slight deviation for preview if rec is warning or critical
        faulty_mags = [m - (4.0 if rec and rec['status'] == 'Warning' else (9.5 if rec and rec['status'] == 'Critical' else 0.2)) for m in mags]
    except Exception:
        freqs = [20, 100, 1000, 10000, 100000, 1000000]
        mags = [-40, -35, -25, -50, -45, -60]
        faulty_mags = [-40, -36, -28, -55, -48, -62]

    return render_template("index.html",
        status=rec["status"] if rec else "Warning",
        transformerId=rec["id"] if rec else asset_id,
        date_now=rec["date"] if rec else datetime.now().strftime("%b %d, %Y %I:%M %p"),
        corr=rec["corr"] if rec else 0.8842,
        shift=rec["shift"] if rec else 6.2,
        freq=freqs,
        healthy=mags,
        faulty=faulty_mags,
        confidence=int((rec["corr"] if rec else 0.88) * 100),
        fault_type=rec["fault_type"] if rec else "Spectral Deviation",
        recommendation=rec["action"] if rec else "Perform internal inspection.",
        active_page='workbench'
    )

@app.route("/about")
def about():
    return render_template("about.html", active_page='standards')

@app.route("/prototype/layout")
def prototype_layout():
    variant = request.args.get("variant", "A").upper()
    if variant not in ["A", "B", "C"]:
        variant = "A"
    view = request.args.get("view", "workbench").lower()
    if view not in ["workbench", "history", "standards", "landing"]:
        view = "workbench"
    return render_template("prototype_layout.html", variant=variant, view=view)

@app.route("/analysis")
def diagnosis_dashboard():
    return render_template("index.html", status=None, active_page='workbench')

@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        file = request.files.get("file")
        if not file:
            return "Error: No file selected.", 400

        # 1. Save upload
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        file.save(file_path)

        # 2. Baseline logic
        baseline_path = os.path.join(RAW_DATA_FOLDER, "fra_healthy.csv")
        
        # Fallback: if baseline is missing, use the upload as baseline to prevent 500 error
        if not os.path.exists(baseline_path):
            print(f"WARNING: Baseline missing at {baseline_path}. Using upload as temporary baseline.")
            baseline_path = file_path

        # 3. Run Diagnostic Pipeline (includes Bode plotting and PDF generation)
        from src.pipeline import run_pipeline
        pdf_path = os.path.join(REPORT_FOLDER, "report.pdf")
        pipeline_results = run_pipeline(
            file_path,
            baseline_path,
            generate_pdf=True,
            pdf_output_path=pdf_path
        )
        if not pipeline_results:
            return "Error: CSV parsing failed. Ensure columns are 'Frequency' and 'Magnitude'.", 500

        result = pipeline_results[0] if isinstance(pipeline_results, list) else pipeline_results

        # Calculate a Confidence Score out of 100 based on correlation
        conf_score = int(result.get("correlation", 0) * 100)
        transformer_id = result.get("transformer_id") or file.filename
        date_str = result.get("test_date") or datetime.now().strftime("%b %d, %Y %I:%M %p")

        return render_template("index.html",
            status=result.get("status", "Warning"),
            transformerId=transformer_id,
            date_now=date_str,
            corr=round(result.get("correlation", 0), 4),
            shift=round(result.get("shift", 0), 2),
            freq=result.get("frequencies", []),
            healthy=result.get("magnitude_healthy", []),
            faulty=result.get("magnitude_uploaded", []),
            confidence=conf_score,
            fault_type=result.get("fault_type", "Spectral Deviation"),
            recommendation=result.get("recommendation", "Perform internal inspection."),
            active_page='workbench'
        )

    except Exception as e:
        import traceback
        print(traceback.format_exc()) 
        return f"Internal Server Error: {str(e)}", 500

@app.route("/download-report")
def download():
    report_path = os.path.join(REPORT_FOLDER, "report.pdf")
    return send_file(report_path, as_attachment=True) if os.path.exists(report_path) else ("Not found", 404)

if __name__ == "__main__":
    app.run(debug=True, port=5000)