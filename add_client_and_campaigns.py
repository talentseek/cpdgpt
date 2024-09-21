from app import create_app
from app.extensions import db
from app.models import Client, Campaign

app = create_app()

with app.app_context():
    # Create a new client for MailMonitor
    mailmonitor = Client(
        business_name="MailMonitor",
        description="Email deliverability app."
    )
    
    # Add the client to the session
    db.session.add(mailmonitor)
    db.session.commit()  # Commit to generate an ID for the client

    # List of campaign IDs for the client
    campaign_ids = [601254, 601253, 511819, 440935, 440873, 274723, 176021, 125526]

    # Create and add campaigns for the client
    for campaign_id in campaign_ids:
        campaign = Campaign(
            id=campaign_id,  # Set the campaign ID
            name=f"Campaign {campaign_id}",
            client_id=mailmonitor.id  # Associate with the MailMonitor client
        )
        db.session.add(campaign)

    # Commit all changes to the database
    db.session.commit()
    print(f"Client 'MailMonitor' and its campaigns have been added to the database.")
