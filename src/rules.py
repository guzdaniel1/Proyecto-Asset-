import pandas as pd


def detect_inconsistencies(df):
    issues = []

    for _, row in df.iterrows():
        issue = None

        status = row.get("status")
        days = row.get("days_in_state")
        location = row.get("location")

        # =========================
        #  Rule 1: Transit > 30 days
        # =========================
        if status == "In Transit" and days > 30:
            issue = "Transit > 30 days"

        # =========================
        #  Rule 2: Transit > 15 days
        # =========================
        elif status == "In Transit" and days > 15:
            issue = "Transit > 15 days"

        # =========================
        #  Rule 3: Invalid status
        # =========================
        elif status not in ["In Stock", "In Transit", "In Use", "Repair"]:
            issue = "Invalid status"

        # =========================
        #  Rule 4: Missing location
        # =========================
        elif not location or pd.isna(location):
            issue = "Missing location"

        issues.append({
            "asset_id": row.get("asset_id"),
            "status": status,
            "days_in_state": days,
            "issue": issue
        })

    return pd.DataFrame(issues)