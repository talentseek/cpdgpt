from flask import Blueprint, request, jsonify, render_template, redirect, url_for
from app.models import Lead, LeadAction, LeadNote, db, Campaign, Client
from sqlalchemy.exc import IntegrityError
from datetime import datetime, date
from sqlalchemy import func

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
    lead_status = data.get('lead_status', 'Interested - Initial Info Requested')
    sl_lead_id = data.get('sl_lead_id')  # Make sure this is captured correctly

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
        campaign_id=campaign_id,
        lead_status=lead_status,
        sl_lead_id=sl_lead_id  # Store Smartlead's lead_id
    )

    try:
        db.session.add(new_lead)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Failed to store the lead due to database error"}), 500

    return jsonify({"message": "Lead stored successfully", "lead": new_lead.to_dict()}), 201

# Route to add a lead (not in Smartlead) to the database
@lead_management_blueprint.route('/add_lead', methods=['POST'])
def add_lead():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    company_name = request.form.get('company_name')
    phone_number = request.form.get('phone_number')
    location = request.form.get('location')
    linkedin_profile = request.form.get('linkedin_profile')
    campaign_id = request.form.get('campaign_id')
    lead_status = request.form.get('lead_status')

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
        phone_number=phone_number,
        location=location,
        linkedin_profile=linkedin_profile,
        campaign_id=campaign_id,
        lead_status=lead_status
    )

    try:
        # Add the lead to the session and commit to the database
        db.session.add(new_lead)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"error": "Failed to store the lead due to database error"}), 500

    return redirect(url_for('lead_management.display_stored_leads'))

# Route to view and manage a specific lead
@lead_management_blueprint.route('/lead/<int:lead_id>', methods=['GET', 'POST'])
def lead_detail(lead_id):
    lead = Lead.query.get(lead_id)
    if not lead:
        return jsonify({"error": "Lead not found"}), 404

    if request.method == 'POST':
        # Update lead status
        new_status = request.form.get('lead_status')
        if new_status:
            lead.lead_status = new_status
            db.session.commit()

    return render_template('lead_detail.html', lead=lead)

# Route to mark an action as complete
@lead_management_blueprint.route('/complete_action/<int:action_id>', methods=['POST'])
def complete_action(action_id):
    action = LeadAction.query.get(action_id)
    if not action:
        return jsonify({"error": "Action not found"}), 404

    action.action_state = 'Done'
    try:
        db.session.commit()
        return redirect(url_for('lead_management.lead_detail', lead_id=action.lead_id))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to mark action as complete: {str(e)}"}), 500

# Route to add an action to a lead
@lead_management_blueprint.route('/add_action/<int:lead_id>', methods=['POST'])
def add_action(lead_id):
    lead = Lead.query.get(lead_id)
    if not lead:
        return jsonify({"error": "Lead not found"}), 404

    action_type = request.form.get('action_type')
    action_description = request.form.get('action_description')
    action_date = request.form.get('action_date')

    if not action_type:
        return jsonify({"error": "Action type is required"}), 400

    # Convert action_date string to a datetime object
    if action_date:
        try:
            action_date = datetime.strptime(action_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    new_action = LeadAction(
        lead_id=lead.id,
        action_type=action_type,
        action_description=action_description,
        action_date=action_date,
        action_state='To do'
    )
    try:
        db.session.add(new_action)
        db.session.commit()
        return redirect(url_for('lead_management.lead_detail', lead_id=lead_id))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add action: {str(e)}"}), 500

# Route to edit an action
@lead_management_blueprint.route('/edit_action/<int:action_id>', methods=['POST'])
def edit_action(action_id):
    action = LeadAction.query.get(action_id)
    if not action:
        return jsonify({"error": "Action not found"}), 404

    action_type = request.form.get('action_type')
    action_description = request.form.get('action_description')
    action_date = request.form.get('action_date')

    if action_type:
        action.action_type = action_type
    if action_description:
        action.action_description = action_description
    if action_date:
        try:
            action.action_date = datetime.strptime(action_date, "%Y-%m-%d")
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD."}), 400

    try:
        db.session.commit()
        return redirect(url_for('lead_management.lead_detail', lead_id=action.lead_id))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to edit action: {str(e)}"}), 500

# Route to delete an action by ID
@lead_management_blueprint.route('/delete_action/<int:action_id>', methods=['POST'])
def delete_action(action_id):
    action = LeadAction.query.get(action_id)

    if not action:
        return jsonify({"error": "Action not found"}), 404

    try:
        db.session.delete(action)
        db.session.commit()
        return redirect(url_for('lead_management.lead_detail', lead_id=action.lead_id))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete action: {str(e)}"}), 500

# Route to add a note to a lead
@lead_management_blueprint.route('/add_note/<int:lead_id>', methods=['POST'])
def add_note(lead_id):
    lead = Lead.query.get(lead_id)
    if not lead:
        return jsonify({"error": "Lead not found"}), 404

    note_content = request.form.get('note')
    if not note_content:
        return jsonify({"error": "Note content is required"}), 400

    new_note = LeadNote(
        lead_id=lead.id,
        note=note_content
    )
    try:
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('lead_management.lead_detail', lead_id=lead_id))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to add note: {str(e)}"}), 500

# Route to edit a note
@lead_management_blueprint.route('/edit_note/<int:note_id>', methods=['POST'])
def edit_note(note_id):
    note = LeadNote.query.get(note_id)
    if not note:
        return jsonify({"error": "Note not found"}), 404

    note_content = request.form.get('note')
    if note_content:
        note.note = note_content

    try:
        db.session.commit()
        return redirect(url_for('lead_management.lead_detail', lead_id=note.lead_id))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to edit note: {str(e)}"}), 500

# Route to delete a note by ID
@lead_management_blueprint.route('/delete_note/<int:note_id>', methods=['POST'])
def delete_note(note_id):
    note = LeadNote.query.get(note_id)

    if not note:
        return jsonify({"error": "Note not found"}), 404

    try:
        db.session.delete(note)
        db.session.commit()
        return redirect(url_for('lead_management.lead_detail', lead_id=note.lead_id))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete note: {str(e)}"}), 500

# Route to update a lead's status
@lead_management_blueprint.route('/update_lead_status/<int:lead_id>', methods=['POST'])
def update_lead_status(lead_id):
    lead = Lead.query.get(lead_id)
    if not lead:
        return jsonify({"error": "Lead not found"}), 404

    new_status = request.form.get('lead_status')

    if not new_status:
        return jsonify({"error": "Lead status is required"}), 400

    lead.lead_status = new_status

    try:
        db.session.commit()
        return redirect(url_for('lead_management.all_actions'))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to update lead status: {str(e)}"}), 500

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

# Route to display all actions with optional filtering by action state
@lead_management_blueprint.route('/all_actions', methods=['GET'])
def all_actions():
    action_state = request.args.get('action_state')  # Get action_state from query params
    query = LeadAction.query.options(db.joinedload(LeadAction.lead))
    if action_state:
        query = query.filter_by(action_state=action_state)
    actions = query.all()
    return render_template('actions.html', actions=actions)

# Route to display actions due today with optional filtering by action state
@lead_management_blueprint.route('/due_today', methods=['GET'])
def due_today():
    today = date.today()
    action_state = request.args.get('action_state')
    query = LeadAction.query.filter(func.date(LeadAction.action_date) == today).options(db.joinedload(LeadAction.lead))
    if action_state:
        query = query.filter_by(action_state=action_state)
    actions = query.all()
    return render_template('actions.html', actions=actions)

# Route to display overdue actions with optional filtering by action state
@lead_management_blueprint.route('/overdue', methods=['GET'])
def overdue():
    today = date.today()
    action_state = request.args.get('action_state')
    query = LeadAction.query.filter(LeadAction.action_date < today, LeadAction.action_state != 'Done').options(db.joinedload(LeadAction.lead))
    if action_state:
        query = query.filter_by(action_state=action_state)
    actions = query.all()
    return render_template('actions.html', actions=actions)

# Route to display upcoming actions with optional filtering by action state
@lead_management_blueprint.route('/upcoming', methods=['GET'])
def upcoming():
    today = date.today()
    action_state = request.args.get('action_state')
    query = LeadAction.query.filter(LeadAction.action_date > today).options(db.joinedload(LeadAction.lead))
    if action_state:
        query = query.filter_by(action_state=action_state)
    actions = query.all()
    return render_template('actions.html', actions=actions)

# Route to filter leads by client and/or lead status
@lead_management_blueprint.route('/filter_leads', methods=['GET'])
def filter_leads():
    client_name = request.args.get('client_name')
    lead_status = request.args.get('lead_status')

    query = Lead.query.join(Campaign).join(Client)

    # Apply filters based on the query parameters
    if client_name:
        query = query.filter(Client.business_name.ilike(f"%{client_name}%"))
    if lead_status:
        query = query.filter(Lead.lead_status == lead_status)

    leads = query.options(db.joinedload(Lead.actions)).all()

    return render_template('leads.html', leads=leads)

# Route to delete a lead by ID
@lead_management_blueprint.route('/delete_lead/<int:lead_id>', methods=['POST'])
def delete_lead(lead_id):
    lead = Lead.query.get(lead_id)

    if not lead:
        return jsonify({"error": "Lead not found"}), 404

    try:
        db.session.delete(lead)
        db.session.commit()
        return redirect(url_for('lead_management.all_actions'))
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Failed to delete lead: {str(e)}"}), 500
