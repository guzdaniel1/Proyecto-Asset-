import pandas as pd
from analyzer import analyze_data
from ai_module import prioritize_cases

def main():
    assets = pd.read_csv("data/assets.csv")
    movements = pd.read_csv("data/movements.csv")
    status = pd.read_csv("data/status_history.csv")

    results = analyze_data(assets, movements, status)

    # IA: priorización
    results = prioritize_cases(results)

    results.to_csv("output/results.csv", index=False)
    print("✅ Análisis completado. Archivo generado en /output/results.csv")

if __name__ == "__main__":
    main()