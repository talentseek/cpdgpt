from flask import Blueprint, jsonify
from app.config import Config
import requests

fetch_lead_categories_blueprint = Blueprint('fetch_lead_categories', __name__)

@fetch_lead_categories_blueprint.route('/fetch_lead_categories', methods=['GET'])
def fetch_lead_categories():
    api_key = Config.SMARTLEAD_API_KEY
    if not api_key:
        return jsonify({"error": "API key is missing"}), 400

    url = f"https://server.smartlead.ai/api/v1/leads/fetch-categories?api_key={api_key}"

    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        categories = response.json()
        return jsonify(categories), 200
    else:
        return jsonify({"error": f"Failed to fetch categories: {response.status_code}"}), response.status_code
