import pandas as pd

def transform_gdp_data(data):
    records = data[1]

    cleaned_records = []

    for record in records:
        cleaned_records.append({
            "country": record["country"]["value"],
            "country_code": record["countryiso3code"],
            "indicator": record["indicator"]["value"],
            "indicator_code": record["indicator"]["id"],
            "year": record["date"],
            "value": record["value"]
        })

    df = pd.DataFrame(cleaned_records)

    df["year"] = pd.to_numeric(df["year"])
    df["value"] = pd.to_numeric(df["value"], errors="coerce")

    df=df.dropna(subset = ["value"])
    df = df.sort_values("year")

    return df