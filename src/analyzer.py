import pandas as pd
from rules import detect_inconsistencies


def analyze_data(assets, movements, status):
    # =========================
    # 🧹 Clean unnecessary columns
    # =========================
    status = status.loc[:, ~status.columns.str.contains('^Unnamed')]

    # =========================
    # 📅 Convert date columns
    # =========================
    status["status_date"] = pd.to_datetime(
        status["status_date"], dayfirst=True, errors="coerce"
    )

    # =========================
    # 📊 Get latest status per asset
    # =========================
    latest_status = (
        status.sort_values("status_date")
        .drop_duplicates("asset_id", keep="last")
    )

    # =========================
    # 🔗 Merge datasets
    # =========================
    df = assets.merge(latest_status, on="asset_id", how="left")

    # =========================
    # 🔧 Fix duplicated column names after merge
    # =========================
    df.rename(columns={
        "status_y": "status",
        "status_x": "original_status"
    }, inplace=True)

    # =========================
    # ⏱ Calculate days in current state
    # =========================
    df["days_in_state"] = (
        pd.Timestamp.today() - df["status_date"]
    ).dt.days

    # =========================
    # 🚨 Detect inconsistencies
    # =========================
    return detect_inconsistencies(df)