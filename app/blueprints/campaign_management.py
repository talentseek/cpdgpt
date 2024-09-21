from flask import Blueprint, render_template
from app.models import Campaign

# Define the blueprint for campaign management
campaign_management_blueprint = Blueprint('campaign_management', __name__)

# Route to display all campaigns
@campaign_management_blueprint.route('/campaigns', methods=['GET'])
def display_campaigns():
    campaigns = Campaign.query.all()  # Fetch all campaigns
    return render_template('campaigns.html', campaigns=campaigns)