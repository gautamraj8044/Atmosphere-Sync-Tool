import requests
from typing import Dict, Optional, Tuple
from .weather_reconciler import WeatherReconciler
import os
from dotenv import load_dotenv

class WeatherFetcher:
    def __init__(self):
        self.apis = {
            "openweathermap": {
                "url": "https://api.openweathermap.org/data/2.5/weather",
                "key": os.getenv("OPENWEATHERMAP_API"),
                "params": lambda location: {"q": location, "appid": self.apis["openweathermap"]["key"], "units": "metric"}
            },
            "weatherapi": {
                "url": "https://api.weatherapi.com/v1/current.json",
                "key": os.getenv("WEATHERAPI_API"),
                "params": lambda location: {"key": self.apis["weatherapi"]["key"], "q": location}
            },
            "accuweather": {
                "url": "https://dataservice.accuweather.com/locations/v1/cities/search",
                "key": os.getenv("ACCUWEATHER_API"),
                "params": lambda location: {"apikey": self.apis["accuweather"]["key"], "q": location}
            }
        }

    def fetch_weather(self, location: str) -> Tuple[Dict, Dict]:
        results = {}
        location_info = {"city": None, "country": None}
        successful_apis = 0
        
        for api, details in self.apis.items():
            try:
                params = details["params"](location)
                response = requests.get(details["url"], params=params, timeout=10)
                response.raise_for_status()
                
                if api == "accuweather":
                    locations = response.json()
                    if locations:
                        location_key = locations[0]["Key"]
                        location_info["city"] = locations[0]["LocalizedName"]
                        location_info["country"] = locations[0]["Country"]["LocalizedName"]
                        conditions_url = f"https://dataservice.accuweather.com/currentconditions/v1/{location_key}"
                        response = requests.get(
                            conditions_url,
                            params={"apikey": details["key"]},
                            timeout=10
                        )
                        response.raise_for_status()
                
                results[api] = response.json()
                
                if not location_info["city"]:
                    if api == "openweathermap":
                        data = response.json()
                        location_info["city"] = data.get("name")
                        location_info["country"] = data.get("sys", {}).get("country")
                    elif api == "weatherapi":
                        data = response.json()
                        location_info["city"] = data.get("location", {}).get("name")
                        location_info["country"] = data.get("location", {}).get("country")
                
                successful_apis += 1
                
            except requests.RequestException as e:
                print(f"Error fetching data from {api}: {str(e)}")
                continue
        
        if successful_apis > 0:
            return results, location_info
        return {}, {}

    def get_weather(self, location: str) -> Dict:
        weather_data, location_info = self.fetch_weather(location)
        if weather_data:
            reconciled_data = WeatherReconciler.reconcile_weather(weather_data)
            if reconciled_data:
                reconciled_data.update(location_info)
                return reconciled_data
                
        return {
            "temperature": None,
            "humidity": None,
            "wind_speed": None,
            "condition": None,
            "city": None,
            "country": None
        }