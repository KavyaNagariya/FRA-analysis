import pandas as pd
import numpy as np
import os

# Create the data folder if it doesn't exist
os.makedirs("data", exist_ok=True)

# Generate a fake "Healthy" transformer curve
freq = np.logspace(1, 6, 200) # 10Hz to 1MHz
# A typical FRA curve shape (simplified)
mag = -20 - (np.sin(np.log10(freq) * 5) * 10) - (np.log10(freq) * 5)

df = pd.DataFrame({'Frequency': freq, 'Magnitude': mag})
df.to_csv("data/fra_healthy.csv", index=False)

print("✅ Success: 'data/fra_healthy.csv' has been created.")