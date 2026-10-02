import numpy as np
import pandas as pd
import os
from src.preprocessor import COMMON_GRID, preprocess_sweep
from src.model import extract_subband_features

def generate_base_response(f, rng):
    magnitude = -20 - 10 * np.log10(f/20 + 1)
    magnitude -= 20 / (1 + ((f - 500) / 100)**2)
    magnitude -= 30 / (1 + ((f - 10000) / 2000)**2)
    magnitude -= 25 / (1 + ((f - 200000) / 50000)**2)
    return magnitude

def generate_dataset():
    rng = np.random.RandomState(42)
    f = COMMON_GRID
    
    n_samples_per_class = 100
    classes = ['Healthy', 'Winding Deformation', 'Insulation Degradation', 'Core Displacement']
    
    features_list = []
    
    for cls in classes:
        for _ in range(n_samples_per_class):
            base_mag = generate_base_response(f, rng)
            base_mag += rng.normal(0, 0.5, size=len(f))
            
            baseline_df = pd.DataFrame({'Frequency': f, 'Magnitude': base_mag})
            test_mag = base_mag.copy()
            
            if cls == 'Healthy':
                test_mag += rng.normal(0, 0.2, size=len(f))
            elif cls == 'Winding Deformation':
                mask = (f >= 2000) & (f <= 100000)
                shift = rng.uniform(3, 15) * np.sin(np.pi * (f - 2000) / 98000)
                test_mag[mask] += shift[mask]
            elif cls == 'Insulation Degradation':
                mask = (f >= 100000) & (f <= 1000000)
                shift = rng.uniform(1, 5) * np.sin(np.pi * (f - 100000) / 900000)
                test_mag[mask] += shift[mask]
            elif cls == 'Core Displacement':
                mask = (f >= 20) & (f <= 2000)
                shift = rng.uniform(5, 20) * np.sin(np.pi * (f - 20) / 1980)
                test_mag[mask] += shift[mask]
                
            test_df = pd.DataFrame({'Frequency': f, 'Magnitude': test_mag})
            
            features = extract_subband_features(baseline_df, test_df)
            features['label'] = cls
            features_list.append(features)
            
    df = pd.DataFrame(features_list)
    os.makedirs('data/processed', exist_ok=True)
    df.to_csv('data/processed/training_features.csv', index=False)
    print(f"Dataset generated at data/processed/training_features.csv with {len(df)} samples.")

if __name__ == "__main__":
    generate_dataset()
