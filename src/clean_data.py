import pandas as pd
import os

def clean_ebird_data(input_path, output_path):
    """
    Clean raw eBird CSV data and save processed version.
    """
    df = pd.read_csv(input_path)
    df = df.dropna(subset=["comName", "lat", "lng"])
    df["obsDt"] = pd.to_datetime(df["obsDt"])
    df = df.rename(columns={"comName": "common_name", "sciName": "scientific_name"})

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"✅ Cleaned data saved to {output_path}")
    return df

if __name__ == "__main__":
    clean_ebird_data("data/raw/ebird_US-IL_20251107.csv", "data/processed/ebird_cleaned.csv")
