def prioritize_cases(df):
    def priority(row):
        if row["issue"] == "Transit > 30 days":
            return "HIGH"
        elif row["issue"] == "Invalid status":
            return "HIGH"
        elif row["issue"] == "Transit > 15 days":
            return "MEDIUM"
        elif row["issue"] == "Missing location":
            return "LOW"
        else:
            return "OK"

    df["priority"] = df.apply(priority, axis=1)
    return df