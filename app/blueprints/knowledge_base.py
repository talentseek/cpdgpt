from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Client, SDR, DetailedDescription
from app.extensions import db

# Define the blueprint for knowledge base management
knowledge_base_blueprint = Blueprint('knowledge_base', __name__)

# Route to display knowledge base for a client
@knowledge_base_blueprint.route('/client/<int:client_id>/knowledge_base', methods=['GET'])
def client_knowledge_base(client_id):
    client = Client.query.get_or_404(client_id)
    sdrs = SDR.query.filter_by(client_id=client_id).all()  # Fetch all SDRs for this client
    detailed_description = DetailedDescription.query.filter_by(client_id=client_id).first()  # Fetch detailed description
    return render_template('client_knowledge_base.html', client=client, sdrs=sdrs, detailed_description=detailed_description)

# Route to add or edit detailed description
@knowledge_base_blueprint.route('/client/<int:client_id>/add_edit_detailed_description', methods=['POST'])
def add_edit_detailed_description(client_id):
    detailed_description = DetailedDescription.query.filter_by(client_id=client_id).first()
    new_description = request.form.get('detailed_description')

    if detailed_description:
        detailed_description.description = new_description
    else:
        detailed_description = DetailedDescription(description=new_description, client_id=client_id)
        db.session.add(detailed_description)

    db.session.commit()
    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to delete detailed description
@knowledge_base_blueprint.route('/client/<int:client_id>/delete_detailed_description', methods=['POST'])
def delete_detailed_description(client_id):
    detailed_description = DetailedDescription.query.filter_by(client_id=client_id).first()
    if detailed_description:
        db.session.delete(detailed_description)
        db.session.commit()
    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to add a new SDR to a client
@knowledge_base_blueprint.route('/client/<int:client_id>/add_sdr', methods=['POST'])
def add_sdr(client_id):
    client = Client.query.get_or_404(client_id)
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    title = request.form.get('title')
    calendar_link = request.form.get('calendar_link')
    rules = request.form.get('rules')

    # Create new SDR
    new_sdr = SDR(
        first_name=first_name,
        last_name=last_name,
        email=email,
        title=title,
        calendar_link=calendar_link,
        rules=rules,
        client_id=client.id
    )

    # Add and commit to the database
    db.session.add(new_sdr)
    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client.id))

# Route to edit an existing SDR
@knowledge_base_blueprint.route('/client/<int:client_id>/edit_sdr/<int:sdr_id>', methods=['POST'])
def edit_sdr(client_id, sdr_id):
    sdr = SDR.query.get_or_404(sdr_id)
    sdr.first_name = request.form.get('first_name')
    sdr.last_name = request.form.get('last_name')
    sdr.email = request.form.get('email')
    sdr.title = request.form.get('title')
    sdr.calendar_link = request.form.get('calendar_link')
    sdr.rules = request.form.get('rules')

    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to delete an SDR
@knowledge_base_blueprint.route('/client/<int:client_id>/delete_sdr/<int:sdr_id>', methods=['POST'])
def delete_sdr(client_id, sdr_id):
    sdr = SDR.query.get_or_404(sdr_id)
    db.session.delete(sdr)
    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))