from app import create_app, db
from app.models import Lead
from flask import jsonify

app = create_app()

@app.route('/leads', methods=['GET'])
def get_leads():
    leads = Lead.query.all()
    leads_list = [
        {
            'id': lead.id,
            'first_name': lead.first_name,
            'last_name': lead.last_name,
            'email': lead.email,
            'company_name': lead.company_name,
            'created_at': lead.created_at,
            'phone_number': lead.phone_number
        } for lead in leads
    ]
    return jsonify(leads_list), 200

if __name__ == "__main__":
    app.run(debug=True)
