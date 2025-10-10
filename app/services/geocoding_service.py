import requests
from models.geocoding_result import GeocodingResult

class GeocodingService:
    def __init__(self, api_key):
        self.api_key = api_key
        self.url = "https://maps.googleapis.com/maps/api/geocode/json"

    def get_coordinates(self, address: str):
        params = {
            "address": address,
            "key": self.api_key
        }

        response = requests.get(self.url, params=params)
        data = response.json()

        if response.status_code != 200 or not data.get("results"):
            return None

        result = data["results"][0]
        location = result["geometry"]["location"]

        return GeocodingResult(
            address=result["formatted_address"],
            latitude=location["lat"],
            longitude=location["lng"]
        )
