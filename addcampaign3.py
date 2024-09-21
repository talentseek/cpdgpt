from app import create_app
from app.extensions import db
from app.models import Campaign, Client

app = create_app()

with app.app_context():
    # Find the MailMonitor client by business name
    mailmonitor = Client.query.filter_by(business_name="MailMonitor").first()

    if mailmonitor:
        # Create and add the missing campaign
        new_campaign = Campaign(
            id=3,  # Set the campaign ID
            name="",  # Empty name since there's no name associated
            client_id=mailmonitor.id  # Associate with the MailMonitor client
        )
        db.session.add(new_campaign)

        # Commit the new campaign to the database
        db.session.commit()
        print(f"Campaign '3' has been added to the 'MailMonitor' client.")
    else:
        print("MailMonitor client not found!")
