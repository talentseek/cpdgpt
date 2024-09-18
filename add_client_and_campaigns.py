from app import create_app
from app.extensions import db
from app.models import Client, Campaign

app = create_app()

with app.app_context():
    # Create a new client
    justpark = Client(
        business_name="JustPark",
        description="A platform for finding and booking parking spaces."
    )
    
    # Add the client to the session
    db.session.add(justpark)
    db.session.commit()  # Commit to generate an ID for the client

    # List of campaign IDs for the client
    campaign_ids = [606501, 511787, 263858, 232487, 174746, 151975, 138773, 2]

    # Create and add campaigns for the client
    for campaign_id in campaign_ids:
        campaign = Campaign(
            id=campaign_id,  # Set the campaign ID
            name=f"Campaign {campaign_id}",
            client_id=justpark.id  # Associate with the JustPark client
        )
        db.session.add(campaign)

    # Commit all changes to the database
    db.session.commit()
    print(f"Client 'JustPark' and its campaigns have been added to the database.")
