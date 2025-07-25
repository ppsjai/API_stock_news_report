import requests
from requests import Response
from typing import Dict

def get_country_info(country_name: str) -> Dict[str, str]:
    url: str = f"https://restcountries.com/v3.1/name/{country_name}"
    try:
        response: Response = requests.get(url)
        response.raise_for_status()

        country_data: dict = response.json()[0]
        source: str = "CACHE" if getattr(response, "from_cache", False) else "API"

        return {
            "Source": source,
            "Name": country_data.get("name", {}).get("common", "N/A"),
            "Capital": country_data.get("capital", ["N/A"])[0],
            "Region": country_data.get("region", "N/A"),
            "Population": str(country_data.get("population", "N/A")),
            "Currencies": ", ".join(country_data.get("currencies", {}).keys()),
        }

    except Exception as e:
        return {"Error": str(e)}

def main() -> None:
    while True:
        country: str = input("Enter a country name (or type 'exit' to quit): ").strip()
        if country.lower() == "exit":
            break

        info: dict[str, str] = get_country_info(country)

        print("\nCountry Information:")
        print("----------------------------------------------------------------------------------------------------------------------------------")
        for key, value in info.items():
            print(f"{key}: {value}")
        print()
            print("------------------------------------------------------------------------------------------------------------------------------")

if __name__ == "__main__":
    main()
