from flask import Blueprint, jsonify, request
from app.config import Config
import requests

fetch_lead_blueprint = Blueprint('fetch_lead', __name__)

def fetch_lead_from_smartlead(email):
    api_key = Config.SMARTLEAD_API_KEY
    url = f"https://server.smartlead.ai/api/v1/leads/?api_key={api_key}&email={email}"
    
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        return None

@fetch_lead_blueprint.route('/fetch_lead', methods=['GET'])
def fetch_lead():
    email = request.args.get('email')

    if not email:
        return jsonify({"error": "Email is required"}), 400
    
    lead_data = fetch_lead_from_smartlead(email)
    
    if lead_data:
        refined_data = {
            "lead_id": lead_data.get('id'),
            "first_name": lead_data.get('first_name'),
            "last_name": lead_data.get('last_name'),
            "email": lead_data.get('email'),
            "company_name": lead_data.get('company_name', 'N/A'),
            "created_at": lead_data.get('created_at'),
            "is_unsubscribed": lead_data.get('is_unsubscribed'),
            "phone_number": lead_data.get('phone_number', 'N/A'),
            "location": lead_data.get('location', 'N/A'),
            "linkedin_profile": lead_data.get('linkedin_profile', 'N/A'),
            "campaigns": [
                {
                    "campaign_id": c.get('campaign_id'),
                    "campaign_name": c.get('campaign_name'),
                    "client_id": c.get('client_id'),
                    "lead_category_id": c.get('lead_category_id', 'N/A')
                } for c in lead_data.get('lead_campaign_data', [])
            ]
        }
        return jsonify(refined_data), 200
    else:
        return jsonify({"error": "Lead not found"}), 404
