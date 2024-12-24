from typing import Dict, Optional
from statistics import median
from dotenv import load_dotenv
load_dotenv()

class WeatherReconciler:
    @staticmethod
    def reconcile_weather(data: Dict) -> Optional[Dict]:
        if not data:
            return None
        
        processed_data = {}
        for api, d in data.items():
            try:
                standardized = WeatherReconciler._standardize_data(api, d)
                if standardized:
                    processed_data[api] = standardized
            except Exception as e:
                print(f"Error processing data from {api}: {str(e)}")
                continue
        
        if not processed_data:
            return None

        weights = {
            "openweathermap": 0.4,
            "weatherapi": 0.35,
            "accuweather": 0.25
        }

        available_apis = list(processed_data.keys())
        if available_apis:
            total_weight = sum(weights[api] for api in available_apis)
            adjusted_weights = {api: weights[api]/total_weight for api in available_apis}
        else:
            return None

        temperatures = [d["temperature"] for d in processed_data.values() if d.get("temperature") is not None]
        humidities = [d["humidity"] for d in processed_data.values() if d.get("humidity") is not None]
        wind_speeds = [d["wind_speed"] for d in processed_data.values() if d.get("wind_speed") is not None]
        conditions = [d["condition"] for d in processed_data.values() if d.get("condition")]

        try:
            temperature = round(sum(t * adjusted_weights[api] for api, t in zip(processed_data.keys(), temperatures)), 1) if temperatures else None
            humidity = round(median(humidities)) if humidities else None
            wind_speed = round(max(wind_speeds), 1) if wind_speeds else None
            condition = max(set(conditions), key=conditions.count) if conditions else None
        except Exception as e:
            print(f"Error calculating final values: {str(e)}")
            return None

        return {
            "temperature": temperature,
            "humidity": humidity,
            "wind_speed": wind_speed,
            "condition": condition
        }

    @staticmethod
    def _standardize_data(api: str, data: Dict) -> Optional[Dict]:
        try:
            if api == "openweathermap":
                if not isinstance(data, dict):
                    return None
                    
                temp = data.get("main", {}).get("temp")
                humidity = data.get("main", {}).get("humidity")
                wind_speed = data.get("wind", {}).get("speed")
                condition = data.get("weather", [{}])[0].get("main")
                
                return {
                    "temperature": float(temp) if temp is not None else None,
                    "humidity": float(humidity) if humidity is not None else None,
                    "wind_speed": float(wind_speed) if wind_speed is not None else None,
                    "condition": str(condition) if condition else None
                }
                
            elif api == "weatherapi":
                if not isinstance(data, dict):
                    return None
                    
                current = data.get("current", {})
                temp = current.get("temp_c")
                humidity = current.get("humidity")
                wind_speed = current.get("wind_kph")
                condition = current.get("condition", {}).get("text")
                
                return {
                    "temperature": float(temp) if temp is not None else None,
                    "humidity": float(humidity) if humidity is not None else None,
                    "wind_speed": float(wind_speed) / 3.6 if wind_speed is not None else None,
                    "condition": str(condition) if condition else None
                }
                
            elif api == "accuweather":
                if not isinstance(data, list) or not data:
                    return None
                    
                current = data[0]
                temp = current.get("Temperature", {}).get("Metric", {}).get("Value")
                humidity = current.get("RelativeHumidity")
                wind_speed = current.get("Wind", {}).get("Speed", {}).get("Metric", {}).get("Value")
                condition = current.get("WeatherText")
                
                return {
                    "temperature": float(temp) if temp is not None else None,
                    "humidity": float(humidity) if humidity is not None else None,
                    "wind_speed": float(wind_speed) / 3.6 if wind_speed is not None else None,
                    "condition": str(condition) if condition else None
                }
                
        except Exception as e:
            print(f"Error standardizing data for {api}: {str(e)}")
            return None
            
        return None