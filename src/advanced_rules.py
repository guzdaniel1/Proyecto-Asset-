import pandas as pd


def detect_advanced_inconsistencies(assets, movements, status):
    """
    Analyze advanced inconsistencies by combining:
    - current status
    - latest movements
    - asset data

    Returns a DataFrame with:
    asset_id | type | detail | priority
    """

    issues = []
    today = pd.Timestamp.today()

    # =========================
    #  DATA CLEANING
    # =========================

    # remove unwanted columns (e.g., Unnamed)
    status = status.loc[:, ~status.columns.str.contains('^Unnamed')]
    movements = movements.loc[:, ~movements.columns.str.contains('^Unnamed')]

    # safely convert dates
    status["status_date"] = pd.to_datetime(
        status["status_date"], errors="coerce", dayfirst=True
    )
    movements["movement_date"] = pd.to_datetime(
        movements["movement_date"], errors="coerce", dayfirst=True
    )

    # =========================
    #  LATEST RECORDS
    # =========================

    latest_status = (
        status.sort_values("status_date")
        .drop_duplicates("asset_id", keep="last")
    )

    latest_movement = (
        movements.sort_values("movement_date")
        .drop_duplicates("asset_id", keep="last")
    )

    # =========================
    #  MERGES
    # =========================

    df = assets.merge(
        latest_status,
        on="asset_id",
        how="left",
        suffixes=("_asset", "_status")
    )

    df = df.merge(
        latest_movement[["asset_id", "movement_date"]],
        on="asset_id",
        how="left"
    )

    # =========================
    #  FIELD NORMALIZATION
    # =========================

    if "status_status" in df.columns:
        df["final_status"] = df["status_status"]
    elif "status" in df.columns:
        df["final_status"] = df["status"]
    else:
        df["final_status"] = None

    # =========================
    #  ADVANCED RULES
    # =========================

    for _, row in df.iterrows():

        asset_id = row.get("asset_id")

        status_val = str(row.get("final_status") or "").lower()
        location = str(row.get("location") or "").lower()

        assigned = row.get("assigned_to")
        has_assignment = pd.notna(assigned) and str(assigned).strip() != ""

        last_movement = row.get("movement_date")
        status_date = row.get("status_date")

        # -------------------------
        # Rule 1: Stock in wrong location
        # -------------------------
        if "stock" in status_val and "warehouse" not in location:
            issues.append({
                "asset_id": asset_id,
                "type": "location",
                "detail": "In Stock outside warehouse",
                "priority": "MEDIUM"
            })

        # -------------------------
        # Rule 2: Usage without assignment
        # -------------------------
        if "use" in status_val and not has_assignment:
            issues.append({
                "asset_id": asset_id,
                "type": "assignment",
                "detail": "In use without assignment",
                "priority": "HIGH"
            })

        if "stock" in status_val and has_assignment:
            issues.append({
                "asset_id": asset_id,
                "type": "assignment",
                "detail": "In stock but assigned",
                "priority": "MEDIUM"
            })

        # -------------------------
        # Rule 3: Transit without recent movement
        # -------------------------
        if "transit" in status_val:
            if pd.isna(last_movement) or (today - last_movement).days > 10:
                issues.append({
                    "asset_id": asset_id,
                    "type": "movement",
                    "detail": "No recent movement",
                    "priority": "CRITICAL"
                })

        # -------------------------
        # Rule 4: Prolonged transit
        # -------------------------
        if "transit" in status_val and pd.notna(status_date):
            if (today - status_date).days > 30:
                issues.append({
                    "asset_id": asset_id,
                    "type": "time",
                    "detail": "More than 30 days in transit",
                    "priority": "CRITICAL"
                })

    # =========================
    #  FINAL OUTPUT
    # =========================

    result_df = pd.DataFrame(issues)

    if result_df.empty:
        result_df = pd.DataFrame(columns=["asset_id", "type", "detail", "priority"])

    return result_df