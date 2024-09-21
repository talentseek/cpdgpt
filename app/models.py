from app.extensions import db
from datetime import datetime

# Client model - represents a client or business.
class Client(db.Model):
    __tablename__ = 'clients'
    id = db.Column(db.Integer, primary_key=True)
    business_name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # A client can have multiple campaigns and SDRs.
    campaigns = db.relationship('Campaign', backref='client', lazy=True)
    sdrs = db.relationship('SDR', backref='client', lazy=True)  # New relationship for SDRs

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

# SDR model - represents Sales Development Representatives linked to a client.
class SDR(db.Model):
    __tablename__ = 'sdrs'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    title = db.Column(db.String(100), nullable=True)
    calendar_link = db.Column(db.String(255), nullable=True)
    rules = db.Column(db.Text, nullable=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)  # ForeignKey to Client.

# Detailed Description
class DetailedDescription(db.Model):
    __tablename__ = 'detailed_descriptions'
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id'), nullable=False)  # ForeignKey to Client.
    description = db.Column(db.Text, nullable=False)  # The detailed description content itself.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# Lead model - represents a lead or prospect that is part of a campaign.
class Lead(db.Model):
    __tablename__ = 'leads'
    id = db.Column(db.Integer, primary_key=True)
    sl_lead_id = db.Column(db.Integer, nullable=True)  # Smartlead Lead ID
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
    lead_status = db.Column(db.String(255), nullable=False, default='Interested - Initial Info Requested')  # New field for lead status.

    # A lead can have multiple actions and notes, with cascade delete enabled
    actions = db.relationship('LeadAction', backref='lead', lazy=True, cascade='all, delete-orphan')
    notes = db.relationship('LeadNote', backref='lead', lazy=True, cascade='all, delete-orphan')

    # Method to convert lead data to a dictionary.
    def to_dict(self):
        return {
            'id': self.id,
            'sl_lead_id': self.sl_lead_id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'company_name': self.company_name,
            'created_at': self.created_at,
            'is_unsubscribed': self.is_unsubscribed,
            'phone_number': self.phone_number,
            'location': self.location,
            'linkedin_profile': self.linkedin_profile,
            'campaign_id': self.campaign_id,
            'lead_status': self.lead_status,
            'actions': [action.to_dict() for action in self.actions],
            'notes': [note.to_dict() for note in self.notes],
            'is_in_smartlead': self.sl_lead_id is not None
        }

    @property
    def is_in_smartlead(self):
        return self.sl_lead_id is not None

# LeadAction model - represents actions taken on a lead (e.g., contacting them, marking as demo).
class LeadAction(db.Model):
    __tablename__ = 'lead_actions'
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False)  # ForeignKey to Lead.
    action_type = db.Column(db.String(255), nullable=False)  # Action type (e.g., 'Contacted', 'Demo Booked').
    action_description = db.Column(db.Text, nullable=True)  # Optional description of the action.
    action_date = db.Column(db.DateTime, nullable=True)  # Date for when the action should be completed.
    action_state = db.Column(db.String(50), nullable=False, default='To do')  # State of the action ('Done' or 'To do').
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Method to convert action data to a dictionary.
    def to_dict(self):
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'action_type': self.action_type,
            'action_description': self.action_description,
            'action_date': self.action_date,
            'action_state': self.action_state,
            'created_at': self.created_at
        }

# LeadNote model - represents additional notes added to a lead.
class LeadNote(db.Model):
    __tablename__ = 'lead_notes'
    id = db.Column(db.Integer, primary_key=True)
    lead_id = db.Column(db.Integer, db.ForeignKey('leads.id'), nullable=False)  # ForeignKey to Lead.
    note = db.Column(db.Text, nullable=False)  # The note content itself.
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Method to convert note data to a dictionary.
    def to_dict(self):
        return {
            'id': self.id,
            'lead_id': self.lead_id,
            'note': self.note,
            'created_at': self.created_at
        }