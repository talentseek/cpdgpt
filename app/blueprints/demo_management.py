from flask import Blueprint, request, jsonify
import logging

# Define the blueprint for demo management
demo_management_blueprint = Blueprint('demo_management', __name__)

# Webhook route to handle incoming demo booking data from cal.com
@demo_management_blueprint.route('/webhook', methods=['POST'])
def webhook():
    # Log that the webhook endpoint was hit
    logging.info("Webhook received")

    # Get JSON data from the webhook
    data = request.get_json()

    # Log the incoming JSON for debugging
    logging.info(f"Received Webhook Data: {data}")

    if not data:
        return jsonify({"error": "No data provided"}), 400

    # Extract the payload
    payload = data.get('payload', {})

    # Log the payload for more detailed inspection
    logging.info(f"Payload Data: {payload}")

    # Return the received data as JSON response (just like in your standalone script)
    return jsonify({
        "status": "received",
        "payload": payload
    }), 200
