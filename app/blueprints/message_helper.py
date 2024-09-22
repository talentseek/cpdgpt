from flask import Blueprint, render_template
from app.models import Lead, Client, Campaign, SDR, MoreInformation, CaseStudy

# Define the blueprint for the message helper
message_helper_blueprint = Blueprint('message_helper', __name__)

# Route for message helper page
@message_helper_blueprint.route('/message_helper/<int:lead_id>', methods=['GET'])
def message_helper(lead_id):
    # Fetch the lead and its related campaign information
    lead = Lead.query.get_or_404(lead_id)

    # Assuming Lead has a campaign_id that links to the Campaign
    campaign = Campaign.query.get(lead.campaign_id)

    # Fetch the client related to the campaign
    client = Client.query.filter_by(id=campaign.client_id).first() if campaign else None

    # Fetch SDRs, More Information, and Case Studies for the client
    sdrs = SDR.query.filter_by(client_id=client.id).all() if client else []
    more_information = MoreInformation.query.filter_by(client_id=client.id).all() if client else []
    case_studies = CaseStudy.query.filter_by(client_id=client.id).all() if client else []

    # Extract the client name if available
    client_name = client.business_name if client else 'Unknown'

    # Pass all retrieved data to the template
    return render_template('message_helper.html', lead=lead, client_name=client_name, sdrs=sdrs,
                           more_information=more_information, case_studies=case_studies)