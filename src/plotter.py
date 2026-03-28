import matplotlib
matplotlib.use('Agg')  # Required for non-GUI environments (like Flask)
import matplotlib.pyplot as plt
import io
import base64
import os

# Create a directory for plots if it doesn't exist
PLOT_DIR = "app/static/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

def generate_comparison_plot(data1, data2):
    """
    Generates an overlay plot and returns it as a base64 string 
    for direct embedding in HTML.
    """
    plt.figure(figsize=(10, 5))
    plt.style.use('dark_background') # Matches your dashboard theme

    # Plot Reference (Healthy)
    plt.plot(data1["Frequency"], data1["Magnitude"], 
             label="Baseline (Healthy)", color='#38bdf8', linewidth=1.5, linestyle='--')
    
    # Plot Uploaded (Faulty/Test)
    plt.plot(data2["Frequency"], data2["Magnitude"], 
             label="Test Measurement", color='#f59e0b', linewidth=2)

    plt.xscale('log') # FRA data is almost always viewed on a Log scale
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.title("Frequency Response Analysis - Comparison")
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=0.1)

    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=True)
    plt.close()
    buf.seek(0)
    
    # Encode to base64
    plot_data = base64.b64encode(buf.getvalue()).decode('utf-8')
    return f"data:image/png;base64,{plot_data}"

def save_fra_plot(data, filename="latest_plot.png"):
    """
    Saves a plot to the static folder.
    """
    plt.figure(figsize=(8, 4))
    plt.plot(data["Frequency"], data["Magnitude"], color='#38bdf8')
    plt.xscale('log')
    plt.grid(True)
    
    save_path = os.path.join(PLOT_DIR, filename)
    plt.savefig(save_path)
    plt.close()
    return save_path