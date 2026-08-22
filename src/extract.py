import requests

BASE_URL = "https://api.worldbank.org/v2"

country ="ZAF"
indicator = "NY.GDP.MKTP.CD"

url = f"{BASE_URL}/country/{country}/indicator/{indicator}"


response = requests.get(
    url,
    params={"format": "json"},
    timeout=30
)
response.raise_for_status()

data =response.json()
print(data)