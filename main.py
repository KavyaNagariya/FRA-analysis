from src.data_loader import load_fra_data
from src.analyzer import advanced_analysis

healthy = load_fra_data("data/raw/fra_healthy.csv")
faulty = load_fra_data("data/raw/fra_faulty.csv")

result = advanced_analysis(healthy, faulty)

print(result)