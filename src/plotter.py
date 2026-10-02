import matplotlib
matplotlib.use('Agg')  # Required for non-GUI environments (like Flask)
import matplotlib.pyplot as plt
import io
import base64
import os

# Create a directory for plots if it doesn't exist
PLOT_DIR = "app/static/plots"
os.makedirs(PLOT_DIR, exist_ok=True)

def generate_comparison_plot(data1, data2, theme='dark'):
    """
    Generates an overlay plot and returns it as a base64 string 
    for direct embedding in HTML or PDF reports.
    """
    plt.figure(figsize=(10, 5))
    if theme == 'light':
        plt.style.use('default')
        ref_color = '#0284c7'
        test_color = '#d97706'
        grid_alpha = 0.3
    else:
        plt.style.use('dark_background')
        ref_color = '#38bdf8'
        test_color = '#f59e0b'
        grid_alpha = 0.1

    # Plot Reference (Healthy)
    plt.plot(data1["Frequency"], data1["Magnitude"], 
             label="Baseline (Healthy)", color=ref_color, linewidth=1.5, linestyle='--')
    
    # Plot Uploaded (Faulty/Test)
    plt.plot(data2["Frequency"], data2["Magnitude"], 
             label="Test Measurement", color=test_color, linewidth=2)

    plt.xscale('log') # FRA data is almost always viewed on a Log scale
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude (dB)")
    plt.title("Frequency Response Analysis - Comparison")
    plt.legend()
    plt.grid(True, which="both", ls="-", alpha=grid_alpha)

    # Save to buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', transparent=(theme != 'light'))
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