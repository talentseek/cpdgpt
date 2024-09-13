from flask import Blueprint, request, jsonify, render_template
from app.models import Lead, db
from sqlalchemy.exc import IntegrityError

# Define the blueprint and its URL prefix
lead_management_blueprint = Blueprint('lead_management', __name__)

# Route to store a lead in the database
@lead_management_blueprint.route('/store_lead', methods=['POST'])
def store_lead():
    data = request.get_json()

    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    company_name = data.get('company_name')
    location = data.get('location')
    linkedin_profile = data.get('linkedin_profile')
    phone_number = data.get('phone_number')
    campaign_id = data.get('campaign_id')

    if not email:
        return jsonify({"error": "Email is required"}), 400

    # Check if lead already exists by email
    existing_lead = Lead.query.filter_by(email=email).first()
    if existing_lead:
        return jsonify({"error": "Lead with this email already exists"}), 409

    # Create a new lead instance
    new_lead = Lead(
        email=email,
        first_name=first_name,
        last_name=last_name,
        company_name=company_name,
        location=location,
        linkedin_profile=linkedin_profile,
        phone_number=phone_number,
        campaign_id=campaign_id
    )

    try:
        # Add the lead to the session and commit to the database
        db.session.add(new_lead)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()  # Roll back the session in case of any errors
        return jsonify({"error": "Failed to store the lead due to database error"}), 500

    return jsonify({"message": "Lead stored successfully", "lead": new_lead.to_dict()}), 201

# Route to return stored leads as JSON
@lead_management_blueprint.route('/stored_leads', methods=['GET'])
def get_stored_leads():
    leads = Lead.query.all()  # Retrieve all leads from the database
    lead_data = [lead.to_dict() for lead in leads]  # Use the to_dict() method
    return jsonify(lead_data), 200

# Route to display stored leads in an HTML table
@lead_management_blueprint.route('/display_leads', methods=['GET'])
def display_stored_leads():
    leads = Lead.query.all()  # Retrieve all leads from the database
    return render_template('leads.html', leads=leads)  # Make sure to pass leads to the template
