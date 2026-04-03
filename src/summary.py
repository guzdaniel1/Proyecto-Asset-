import pandas as pd


def generate_summary(results_df):
    summary = {}

    # =========================
    #  GENERAL METRICS
    # =========================
    total_assets = results_df["asset_id"].nunique()
    total_records = len(results_df)

    summary["total_assets"] = total_assets
    summary["total_records"] = total_records

    # =========================
    #  PRIORITIES
    # =========================
    if "priority" in results_df.columns:
        priority_counts = results_df["priority"].value_counts().to_dict()

        for key, value in priority_counts.items():
            summary[f"priority_{key.lower()}"] = value
    else:
        priority_counts = {}

    # =========================
    #  ISSUES
    # =========================
    if "issue" in results_df.columns:
        issue_counts = results_df["issue"].value_counts().to_dict()

        for key, value in issue_counts.items():
            clean_key = key.lower().replace(" ", "_")
            summary[f"issue_{clean_key}"] = value
    else:
        issue_counts = {}

    # =========================
    #  CRITICAL %
    # =========================
    high = priority_counts.get("HIGH", 0)
    total = total_records if total_records > 0 else 1  # avoid division by zero

    critical_pct = (high / total) * 100
    summary["critical_percentage"] = round(critical_pct, 2)

    return pd.DataFrame([summary])


def save_summary(
    results_path="output/results.csv",
    output_path="output/summary.csv"
):
    df = pd.read_csv(results_path)

    summary_df = generate_summary(df)

    summary_df.to_csv(output_path, index=False)

    print(f"Summary generated at: {output_path}")