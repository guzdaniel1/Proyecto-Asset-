import pandas as pd
from rules import detect_inconsistencies

def analyze_data(assets, movements, status):
    df = assets.merge(status, on="asset_id", how="left")

    # calcular días en estado
    df["last_update"] = pd.to_datetime(df["status_date"], dayfirst=True)
    df["days_in_state"] = (pd.Timestamp.today() - df["last_update"]).dt.days

    inconsistencies = detect_inconsistencies(df)

    return inconsistencies