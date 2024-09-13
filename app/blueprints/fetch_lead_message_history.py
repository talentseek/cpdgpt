from flask import Blueprint, jsonify, request
from app.config import Config
import requests

fetch_lead_message_history_blueprint = Blueprint('fetch_lead_message_history', __name__)

@fetch_lead_message_history_blueprint.route('/fetch_lead_message_history', methods=['GET'])
def fetch_lead_message_history():
    campaign_id = request.args.get('campaign_id')
    lead_id = request.args.get('lead_id')
    
    if not campaign_id or not lead_id:
        return jsonify({"error": "Campaign ID and Lead ID are required"}), 400
    
    api_key = Config.SMARTLEAD_API_KEY
    url = f"https://server.smartlead.ai/api/v1/campaigns/{campaign_id}/leads/{lead_id}/message-history?api_key={api_key}"
    
    headers = {"accept": "text/plain"}
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        return jsonify(response.json()), 200
    else:
        return jsonify({"error": f"Failed to fetch message history: {response.status_code}"}), response.status_code
