import pandas as pd
from rules import detect_inconsistencies

def analyze_data(assets, movements, status):

    # limpiar columnas basura
    status = status.loc[:, ~status.columns.str.contains('^Unnamed')]

    # convertir fechas
    status["status_date"] = pd.to_datetime(status["status_date"], dayfirst=True)

    # quedarnos con el último estado por asset
    latest_status = status.sort_values("status_date").drop_duplicates("asset_id", keep="last")

    # merge
    df = assets.merge(latest_status, on="asset_id", how="left")

    # 🔥 ARREGLAR nombres de columnas
    df.rename(columns={
        "status_y": "status",
        "status_x": "original_status"
    }, inplace=True)

    # calcular días en estado
    df["days_in_state"] = (pd.Timestamp.today() - df["status_date"]).dt.days

    return detect_inconsistencies(df)