from flask import Flask
from app.blueprints.fetch_lead import fetch_lead_blueprint
from app.blueprints.fetch_lead_categories import fetch_lead_categories_blueprint
from app.blueprints.fetch_lead_message_history import fetch_lead_message_history_blueprint
from app.blueprints.reply_to_lead import reply_to_lead_blueprint
from app.blueprints.update_lead_category import update_lead_category_blueprint

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(fetch_lead_blueprint)
    app.register_blueprint(fetch_lead_categories_blueprint)
    app.register_blueprint(fetch_lead_message_history_blueprint)
    app.register_blueprint(reply_to_lead_blueprint)
    app.register_blueprint(update_lead_category_blueprint)

    return app
