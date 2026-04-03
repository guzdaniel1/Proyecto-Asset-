import pandas as pd


def generate_summary(results_df):
    summary = {}

    # =========================
    # 📊 MÉTRICAS GENERALES
    # =========================
    total_assets = results_df["asset_id"].nunique()
    total_records = len(results_df)

    summary["total_assets"] = total_assets
    summary["total_records"] = total_records

    # =========================
    # 🔥 PRIORIDADES
    # =========================
    priority_counts = results_df["priority"].value_counts().to_dict()

    for key, value in priority_counts.items():
        summary[f"priority_{key.lower()}"] = value

    # =========================
    # ⚠️ ISSUES
    # =========================
    issue_counts = results_df["issue"].value_counts().to_dict()

    for key, value in issue_counts.items():
        summary[f"issue_{key.lower().replace(' ', '_')}"] = value

    # =========================
    # 🚨 % CRÍTICOS
    # =========================
    high = priority_counts.get("HIGH", 0)
    critical_pct = (high / total_records * 100) if total_records > 0 else 0

    summary["critical_percentage"] = round(critical_pct, 2)

    return pd.DataFrame([summary])


def save_summary(results_path="output/results.csv",
                 output_path="output/summary.csv"):

    df = pd.read_csv(results_path)

    summary_df = generate_summary(df)

    summary_df.to_csv(output_path, index=False)

    print(f"📊 Resumen generado en: {output_path}")