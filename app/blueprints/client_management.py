from flask import Blueprint, render_template
from app.models import Client

# Define the blueprint for client management
client_management_blueprint = Blueprint('client_management', __name__)

# Route to display all clients
@client_management_blueprint.route('/clients', methods=['GET'])
def display_clients():
    clients = Client.query.all()  # Fetch all clients
    return render_template('clients.html', clients=clients)