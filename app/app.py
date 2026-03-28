import os
import sys
import pandas as pd
from flask import Flask, render_template, request, send_file
from datetime import datetime

# Add the root directory to sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(BASE_DIR)

from src.model import load_fra_data
from src.analyzer import advanced_analysis

app = Flask(__name__)

# --- Configure Absolute Paths ---
UPLOAD_FOLDER = os.path.join(BASE_DIR, "data")
RAW_DATA_FOLDER = os.path.join(BASE_DIR, "data", "raw")
REPORT_FOLDER = os.path.join(BASE_DIR, "reports")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(RAW_DATA_FOLDER, exist_ok=True) # Ensure raw folder exists
os.makedirs(REPORT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("landing.html")

@app.route("/history")
def history():
    """FIX: Scans the data directory to show actual uploaded files in the history UI."""
    records = []
    if os.path.exists(UPLOAD_FOLDER):
        # Filter for CSV files and skip directory names
        files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith('.csv') and os.path.isfile(os.path.join(UPLOAD_FOLDER, f))]
        for f in files:
            file_path = os.path.join(UPLOAD_FOLDER, f)
            mtime = os.path.getmtime(file_path)
            records.append({
                "id": f.replace(".csv", ""),
                "date": datetime.fromtimestamp(mtime).strftime("%Y-%m-%d"),
                "status": "Processed" 
            })
    return render_template("history.html", records=records)

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/analysis")
def diagnosis_dashboard():
    return render_template("index.html", status=None)

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

        # 3. Load Data
        uploaded_df = load_fra_data(file_path)
        healthy_df = load_fra_data(baseline_path)

        if uploaded_df is None or healthy_df is None:
            return "Error: CSV parsing failed. Ensure columns are 'Frequency' and 'Magnitude'.", 500

        # 4. Run Analysis
        result = advanced_analysis(healthy_df, uploaded_df)

        # Calculate a Confidence Score out of 100 based on correlation
        conf_score = int(result.get("correlation", 0) * 100)

        return render_template("index.html",
            status=result.get("status", "Warning"),
            transformerId=file.filename,
            date_now=datetime.now().strftime("%b %d, %Y %I:%M %p"),
            corr=round(result.get("correlation", 0), 4),
            shift=round(result.get("shift", 0), 2),
            freq=result.get("frequencies", []),
            healthy=result.get("magnitude_healthy", []),
            faulty=result.get("magnitude_uploaded", []),
            confidence=conf_score,
            fault_type=result.get("fault_type", "Spectral Deviation"),
            recommendation=result.get("recommendation", "Perform internal inspection.")
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