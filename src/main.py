import pandas as pd
from analyzer import analyze_data
from ai_module import prioritize_cases
from advanced_rules import detectar_inconsistencias_avanzadas  #  nuevo

def main():
    assets = pd.read_csv("data/assets.csv", sep=";")
    movements = pd.read_csv("data/movements.csv", sep=";")
    status = pd.read_csv("data/status_history.csv", sep=";")

    # 🔹 análisis base
    results = analyze_data(assets, movements, status)
    results = prioritize_cases(results)

    # 🔹 inconsistencias avanzadas
    inconsistencias = detectar_inconsistencias_avanzadas(assets, movements, status)

    # 🔹 guardar outputs
    results.to_csv("output/results.csv", index=False)
    inconsistencias.to_csv("output/inconsistencias.csv", index=False)

    print("✅ results.csv generado")
    print("✅ inconsistencias.csv generado")

if __name__ == "__main__":
    main()