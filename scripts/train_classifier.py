import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.dataset_generator import generate_dataset
from src.model import train_model

def main():
    print("Generating dataset...")
    generate_dataset()
    
    print("Training model...")
    report, importances = train_model()
    
    print("\n--- Classification Report ---")
    print(report)
    
    print("--- Feature Importances ---")
    print(importances)

if __name__ == "__main__":
    main()
