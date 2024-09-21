from flask import Flask
from app.extensions import db, migrate  # Import from extensions
from app.blueprints.fetch_lead import fetch_lead_blueprint
from app.blueprints.fetch_lead_categories import fetch_lead_categories_blueprint
from app.blueprints.fetch_lead_message_history import fetch_lead_message_history_blueprint
from app.blueprints.reply_to_lead import reply_to_lead_blueprint
from app.blueprints.update_lead_category import update_lead_category_blueprint
from app.blueprints.lead_management import lead_management_blueprint
from app.blueprints.client_management import client_management_blueprint
from app.config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    app.register_blueprint(fetch_lead_blueprint)
    app.register_blueprint(fetch_lead_categories_blueprint)
    app.register_blueprint(fetch_lead_message_history_blueprint)
    app.register_blueprint(reply_to_lead_blueprint)
    app.register_blueprint(update_lead_category_blueprint)
    app.register_blueprint(lead_management_blueprint, url_prefix='/lead_management')
    app.register_blueprint(client_management_blueprint)

    return app
