import requests
from app import create_app  # Import your Flask app
from app.models import Lead, db

# List of email addresses
email_list = [
    'eilish@champinternet.com',
    'joey@performancegolf.com',
    'alyssa@btqrecruit.com'
]

# Initialize the Flask app and push the context
app = create_app()  # Adjust if needed
app.app_context().push()

# Function to fetch lead details from Smartlead
def fetch_lead_details(email):
    # Replace with your Smartlead API URL and key
    api_url = f"https://server.smartlead.ai/api/v1/leads/?api_key=84317e41-800f-43e4-9bed-d00961eae992_yb1fzb8&email={email}"
    response = requests.get(api_url)
    
    if response.status_code == 200:
        lead_data = response.json()
        if 'email' not in lead_data:
            lead_data['email'] = email  # Ensure email is in the lead data
        # Extract the first campaign's id
        campaign_id = None
        if lead_data.get('lead_campaign_data'):
            campaign_id = lead_data['lead_campaign_data'][0].get('campaign_id')
        lead_data['campaign_id'] = campaign_id
        return lead_data
    else:
        print(f"Failed to fetch details for {email}")
        return None

# Function to add lead to the database
def add_lead_to_db(lead_data):
    # Check if the lead already exists in the database
    existing_lead = Lead.query.filter_by(email=lead_data['email']).first()
    if existing_lead:
        print(f"Lead {lead_data['email']} already exists in the database.")
        return
    
    new_lead = Lead(
        email=lead_data['email'],
        first_name=lead_data.get('first_name'),
        last_name=lead_data.get('last_name'),
        company_name=lead_data.get('company_name'),
        linkedin_profile=lead_data.get('linkedin_profile'),
        sl_lead_id=lead_data.get('id'),
        campaign_id=lead_data.get('campaign_id'),
        lead_status=lead_data.get('lead_status', 'Interested - Initial Info Requested')
    )
    
    try:
        db.session.add(new_lead)
        db.session.commit()
        print(f"Lead {lead_data['email']} added successfully.")
    except Exception as e:
        db.session.rollback()
        print(f"Error adding lead {lead_data['email']}: {e}")

# Loop through each email and process
for email in email_list:
    lead_details = fetch_lead_details(email)
    if lead_details:
        add_lead_to_db(lead_details)
