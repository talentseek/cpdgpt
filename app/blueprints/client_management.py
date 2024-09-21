from flask import Blueprint, render_template, request, redirect, url_for  # Ensure necessary imports
from app.models import Client  # Removed SDR import since it's in the knowledge base
from app.extensions import db  # Ensure db is imported for database operations

# Define the blueprint for client management
client_management_blueprint = Blueprint('client_management', __name__)

# Route to display all clients
@client_management_blueprint.route('/clients', methods=['GET'])
def display_clients():
    clients = Client.query.all()  # Fetch all clients
    return render_template('clients.html', clients=clients)

# Route to display client detail overview
@client_management_blueprint.route('/client/<int:client_id>', methods=['GET'])
def client_detail(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template('client_detail.html', client=client)

# Route to display contracts and billing for a client
@client_management_blueprint.route('/client/<int:client_id>/contracts_billing', methods=['GET'])
def client_contracts_billing(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template('client_contracts_billing.html', client=client)

# Route to display access and accounts for a client
@client_management_blueprint.route('/client/<int:client_id>/access_accounts', methods=['GET'])
def client_access_accounts(client_id):
    client = Client.query.get_or_404(client_id)
    return render_template('client_access_accounts.html', client=client)

# Route to handle updating client description
@client_management_blueprint.route('/client/<int:client_id>/edit_description', methods=['POST'])
def edit_client_description(client_id):
    client = Client.query.get_or_404(client_id)
    new_description = request.form.get('description')

    if new_description:
        client.description = new_description
        db.session.commit()

    return redirect(url_for('client_management.client_detail', client_id=client.id))