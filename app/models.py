from app.extensions import db
from datetime import datetime

# Client model - represents a client or business.
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # A client can have multiple campaigns.
    campaigns = db.relationship('Campaign', backref='client', lazy=True)

# Campaign model - represents a specific marketing campaign for a client.
class Campaign(db.Model):
    __tablename__ = 'campaigns'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)  # ForeignKey to Client.
    start_date = db.Column(db.DateTime, nullable=True)
    end_date = db.Column(db.DateTime, nullable=True)

    # A campaign can have multiple leads.
    leads = db.relationship('Lead', backref='campaign', lazy=True)

# Lead model - represents a lead or prospect that is part of a campaign.
class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)  # Unique email to prevent duplicates.
    company_name = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_unsubscribed = db.Column(db.Boolean, default=False)
    phone_number = db.Column(db.String(50), nullable=True)
    location = db.Column(db.String(255), nullable=True)
    linkedin_profile = db.Column(db.String(255), nullable=True)
    campaign_id = db.Column(db.Integer, db.ForeignKey('campaigns.id'), nullable=False)  # ForeignKey to Campaign.

    # A lead can have multiple actions and notes.
    actions = db.relationship('LeadAction', backref='lead', lazy=True)
    notes = db.relationship('LeadNote', backref='lead', lazy=True)

    # Method to convert lead data to a dictionary.
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'company_name': self.company_name,
            'created_at': self.created_at,
            'is_unsubscribed': self.is_unsubscribed,
            'phone_number': self.phone_number,
            'location': self.location,
            'linkedin_profile': self.linkedin_profile,
            'campaign_id': self.campaign_id
        }

# LeadAction model - represents actions taken on a lead (e.g., contacting them, marking as demo).
class LeadAction(db.Model):
    __tablename__ = 'lead_actions'
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False)  # ForeignKey to Lead.
    action_type = db.Column(db.String(255), nullable=False)  # Action type (e.g., 'Contacted', 'Demo Booked').
    action_description = db.Column(db.Text, nullable=True)  # Optional description of the action.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# LeadNote model - represents additional notes added to a lead.
class LeadNote(db.Model):
    __tablename__ = 'lead_notes'
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False)  # ForeignKey to Lead.
    note = db.Column(db.Text, nullable=False)  # The note content itself.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
