from flask import Blueprint, request, jsonify
from app.config import Config
import requests

reply_to_lead_blueprint = Blueprint('reply_to_lead', __name__)

@reply_to_lead_blueprint.route('/reply_to_lead', methods=['POST'])
def reply_to_lead():
    data = request.get_json()

    # Required parameters
    campaign_id = data.get('campaign_id')
    email_stats_id = data.get('email_stats_id')
    email_body = data.get('email_body')
    reply_message_id = data.get('reply_message_id')
    reply_email_time = data.get('reply_email_time')
    reply_email_body = data.get('reply_email_body')

    # Optional parameters
    cc = data.get('cc', '')
    bcc = data.get('bcc', '')
    add_signature = data.get('add_signature', True)
    to_first_name = data.get('to_first_name', '')
    to_last_name = data.get('to_last_name', '')
    to_email = data.get('to_email', '')

    if not campaign_id or not email_stats_id or not email_body or not reply_message_id:
        return jsonify({"error": "Missing required fields"}), 400

    api_key = Config.SMARTLEAD_API_KEY
    url = f"https://server.smartlead.ai/api/v1/campaigns/{campaign_id}/reply-email-thread?api_key={api_key}"

    payload = {
        "email_stats_id": email_stats_id,
        "email_body": email_body,
        "reply_message_id": reply_message_id,
        "reply_email_time": reply_email_time,
        "reply_email_body": reply_email_body,
        "cc": cc,
        "bcc": bcc,
        "add_signature": add_signature,
        "to_first_name": to_first_name,
        "to_last_name": to_last_name,
        "to_email": to_email
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json"
    }

    response = requests.post(url, json=payload, headers=headers)

    try:
        if response.headers.get('Content-Type') == 'application/json':
            return jsonify(response.json()), response.status_code
        else:
            return jsonify({"message": response.text}), response.status_code
    except requests.exceptions.JSONDecodeError:
        return jsonify({"error": "Invalid JSON response from Smartlead API", "response_text": response.text}), 500
