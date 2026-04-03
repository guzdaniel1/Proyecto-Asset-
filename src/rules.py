import pandas as pd


def detect_inconsistencies(df):
    issues = []

    for _, row in df.iterrows():
        problem = None

        # Regla 1: In Transit > 30 días
        if row["status"] == "In Transit" and row["days_in_state"] > 30:
            problem = "Transit > 30 days"

        # Regla 2: In Transit > 15 días
        elif row["status"] == "In Transit" and row["days_in_state"] > 15:
            problem = "Transit > 15 days"

        # Regla 3: estado inconsistente
        elif row["status"] not in ["In Stock", "In Transit", "In Use", "Repair"]:
            problem = "Invalid status"

        # Regla 4: sin ubicación
        elif not row.get("location"):
            problem = "Missing location"

        issues.append({
            "asset_id": row["asset_id"],
            "status": row["status"],
            "days_in_state": row["days_in_state"],
            "issue": problem
        })

    return pd.DataFrame(issues)