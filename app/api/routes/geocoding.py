from flask import Flask, request, jsonify
from app.services.geocoding_service import GeocodingService

app = Flask(__name__)

API_KEY = "AIzaSyDfIIPbFtxFmsLEeoe-msMMReXOCPVPBKU"

geocoding_service = GeocodingService(API_KEY)

@app.route("/geocode", methods=["POST"])
def geocode():
    data = request.get_json()
    if not data or "address" not in data:
        return jsonify({"error": "Falta el campo 'address'"}), 400

    result = geocoding_service.get_coordinates(data["address"])
    if not result:
        return jsonify({"error": "No se encontraron coordenadas"}), 404

    return jsonify(result.to_dict())

if __name__ == "__main__":
    app.run(debug=True)
