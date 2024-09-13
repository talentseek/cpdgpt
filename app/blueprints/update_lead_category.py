from flask import Blueprint, request, jsonify
import requests
from app.config import Config

update_lead_category_blueprint = Blueprint('update_lead_category', __name__)

@update_lead_category_blueprint.route('/update_lead_category', methods=['POST'])
def update_lead_category():
    data = request.get_json()

    campaign_id = data.get('campaign_id')
    lead_id = data.get('lead_id')
    category_id = data.get('category_id')
    pause_lead = data.get('pause_lead', False)

    if not campaign_id or not lead_id or not category_id:
        return jsonify({"error": "Missing required fields"}), 400

    api_key = Config.SMARTLEAD_API_KEY
    url = f"https://server.smartlead.ai/api/v1/campaigns/{campaign_id}/leads/{lead_id}/category?api_key={api_key}"

    payload = {
        "category_id": category_id,
        "pause_lead": pause_lead
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": f"Failed to update lead category: {response.status_code}"}), response.status_code
