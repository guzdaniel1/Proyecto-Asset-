import pandas as pd


def detectar_inconsistencias_avanzadas(assets, movements, status):
    """
    Analiza inconsistencias avanzadas combinando:
    - estado actual
    - últimos movimientos
    - datos del asset

    Retorna un DataFrame con:
    asset_id | tipo | detalle | prioridad
    """

    issues = []
    today = pd.Timestamp.today()

    # =========================
    # 🧹 LIMPIEZA DE DATOS
    # =========================

    # eliminar columnas basura tipo Unnamed
    status = status.loc[:, ~status.columns.str.contains('^Unnamed')]
    movements = movements.loc[:, ~movements.columns.str.contains('^Unnamed')]

    # convertir fechas de forma segura
    status["status_date"] = pd.to_datetime(
        status["status_date"], errors="coerce", dayfirst=True
    )
    movements["movement_date"] = pd.to_datetime(
        movements["movement_date"], errors="coerce", dayfirst=True
    )

    # =========================
    # 📊 ÚLTIMOS REGISTROS
    # =========================

    latest_status = (
        status.sort_values("status_date")
        .drop_duplicates("asset_id", keep="last")
    )

    latest_move = (
        movements.sort_values("movement_date")
        .drop_duplicates("asset_id", keep="last")
    )

    # =========================
    # 🔗 MERGES CONTROLADOS
    # =========================

    df = assets.merge(
        latest_status,
        on="asset_id",
        how="left",
        suffixes=("_asset", "_status")
    )

    df = df.merge(
        latest_move[["asset_id", "movement_date"]],
        on="asset_id",
        how="left"
    )

    # =========================
    # 🧠 NORMALIZACIÓN DE CAMPOS
    # =========================

    # detectar columna correcta de status
    if "status_status" in df.columns:
        df["status_final"] = df["status_status"]
    elif "status" in df.columns:
        df["status_final"] = df["status"]
    else:
        df["status_final"] = None

    # =========================
    # 🔍 REGLAS AVANZADAS
    # =========================

    for _, row in df.iterrows():

        asset_id = row.get("asset_id")

        status_val = str(row.get("status_final") or "").lower()
        location = str(row.get("location") or "").lower()

        assigned = row.get("assigned_to")
        has_assigned = pd.notna(assigned) and str(assigned).strip() != ""

        last_move = row.get("movement_date")
        status_date = row.get("status_date")

        # -------------------------
        # Regla 1: Stock mal ubicado
        # -------------------------
        if "stock" in status_val and "warehouse" not in location:
            issues.append({
                "asset_id": asset_id,
                "tipo": "ubicacion",
                "detalle": "In Stock fuera de deposito",
                "prioridad": "MEDIA"
            })

        # -------------------------
        # Regla 2: Uso sin asignación
        # -------------------------
        if "use" in status_val and not has_assigned:
            issues.append({
                "asset_id": asset_id,
                "tipo": "asignacion",
                "detalle": "En uso sin asignacion",
                "prioridad": "ALTA"
            })

        if "stock" in status_val and has_assigned:
            issues.append({
                "asset_id": asset_id,
                "tipo": "asignacion",
                "detalle": "En stock pero asignado",
                "prioridad": "MEDIA"
            })

        # -------------------------
        # Regla 3: Transit sin movimiento
        # -------------------------
        if "transit" in status_val:
            if pd.isna(last_move) or (today - last_move).days > 10:
                issues.append({
                    "asset_id": asset_id,
                    "tipo": "movimiento",
                    "detalle": "Sin movimiento reciente",
                    "prioridad": "CRITICA"
                })

        # -------------------------
        # Regla 4: Transit prolongado
        # -------------------------
        if "transit" in status_val and pd.notna(status_date):
            if (today - status_date).days > 30:
                issues.append({
                    "asset_id": asset_id,
                    "tipo": "tiempo",
                    "detalle": "Más de 30 días en tránsito",
                    "prioridad": "CRITICA"
                })

    # =========================
    # 📦 RESULTADO FINAL
    # =========================

    result_df = pd.DataFrame(issues)

    # evitar DataFrame vacío sin columnas
    if result_df.empty:
        result_df = pd.DataFrame(columns=["asset_id", "tipo", "detalle", "prioridad"])

    return result_df