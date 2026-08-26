import requests

BASE_URL = "https://api.worldbank.org/v2"

def extract_gdp_data():
    country ="ZAF"
    indicator = "NY.GDP.MKTP.CD"

    url = f"{BASE_URL}/country/{country}/indicator/{indicator}"


    response = requests.get(
        url,
        params={"format": "json",
                "per_page": 100},
        timeout=30
    )
    response.raise_for_status()

    return response.json()
    