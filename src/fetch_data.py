import requests
import pandas as pd
from datetime import datetime
import os

def fetch_ebird_data(region="US-IL", api_key="3g5voge8rcai"):
    """
    Fetch recent bird observations for a given region from eBird API.
    region: eBird region code (e.g., 'US-IL' for Illinois)
    api_key: your eBird API token
    """
    url = f"https://api.ebird.org/v2/data/obs/{region}/recent"
    headers = {"X-eBirdApiToken": api_key}

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise Exception(f"Error {response.status_code}: {response.text}")

    data = response.json()
    df = pd.DataFrame(data)

    # 确保保存路径存在
    os.makedirs("data/raw", exist_ok=True)

    filename = f"data/raw/ebird_{region}_{datetime.now().strftime('%Y%m%d')}.csv"
    df.to_csv(filename, index=False)
    print(f"✅ Data saved to {filename}")

    return df

if __name__ == "__main__":
    df = fetch_ebird_data("US-IL")  # Illinois example
    print(df.head(10)[["comName", "sciName", "howMany", "locName", "lat", "lng", "obsDt"]])
