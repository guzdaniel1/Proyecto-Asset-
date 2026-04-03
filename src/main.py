import pandas as pd
from analyzer import analyze_data
from ai_module import prioritize_cases
from advanced_rules import detect_advanced_inconsistencies
from summary import save_summary


def main():
    # =========================
    #  Load input data
    # =========================
    assets = pd.read_csv("data/assets.csv", sep=";")
    movements = pd.read_csv("data/movements.csv", sep=";")
    status = pd.read_csv("data/status_history.csv", sep=";")

    # =========================
    #  Run base analysis
    # =========================
    results = analyze_data(assets, movements, status)

    # =========================
    #  Apply prioritization logic
    # =========================
    results = prioritize_cases(results)

    # =========================
    #  Run advanced inconsistency checks
    # =========================
    advanced_issues = detect_advanced_inconsistencies(
        assets, movements, status
    )

    # =========================
    #  Save outputs
    # =========================
    results.to_csv("output/results.csv", index=False)
    advanced_issues.to_csv("output/detect_advanced_inconsistencies.csv", index=False)

    # =========================
    # Generate summary report
    # =========================
    save_summary()

    # =========================
    #  Execution status
    # =========================
    print("results.csv generated")
    print("advanced_issues.csv generated")
    print("summary.csv generated")


if __name__ == "__main__":
    main()