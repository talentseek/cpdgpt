from flask import Blueprint, render_template, request, redirect, url_for
from app.models import Client, SDR, DetailedDescription, MoreInformation, CaseStudy, ProblemSolution, NoteworthyClient, Feature
from app.extensions import db

# Define the blueprint for knowledge base management
knowledge_base_blueprint = Blueprint('knowledge_base', __name__)

# Route to display knowledge base for a client
@knowledge_base_blueprint.route('/client/<int:client_id>/knowledge_base', methods=['GET'])
def client_knowledge_base(client_id):
    client = Client.query.get_or_404(client_id)
    sdrs = SDR.query.filter_by(client_id=client_id).all()
    detailed_description = DetailedDescription.query.filter_by(client_id=client_id).first()
    more_information = MoreInformation.query.filter_by(client_id=client_id).all()
    case_studies = CaseStudy.query.filter_by(client_id=client_id).all()
    problems_solutions = ProblemSolution.query.filter_by(client_id=client_id).all()
    noteworthy_clients = NoteworthyClient.query.filter_by(client_id=client_id).all()
    features = Feature.query.filter_by(client_id=client_id).all()

    return render_template('client_knowledge_base.html', client=client, sdrs=sdrs, detailed_description=detailed_description,
                           more_information=more_information, case_studies=case_studies, problems_solutions=problems_solutions,
                           noteworthy_clients=noteworthy_clients, features=features)

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

# Route to add an SDR
@knowledge_base_blueprint.route('/client/<int:client_id>/add_sdr', methods=['POST'])
def add_sdr(client_id):
    client = Client.query.get_or_404(client_id)
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    email = request.form.get('email')
    title = request.form.get('title')
    calendar_link = request.form.get('calendar_link')
    rules = request.form.get('rules')

    new_sdr = SDR(client_id=client.id, first_name=first_name, last_name=last_name, email=email, title=title,
                  calendar_link=calendar_link, rules=rules)
    
    db.session.add(new_sdr)
    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client.id))

# Route to edit an SDR
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

# Route to add more information
@knowledge_base_blueprint.route('/client/<int:client_id>/add_more_info', methods=['POST'])
def add_more_info(client_id):
    info_type = request.form.get('info_type')
    link = request.form.get('link')
    rules = request.form.get('rules')

    more_info = MoreInformation(client_id=client_id, info_type=info_type, link=link, rules=rules)
    db.session.add(more_info)
    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to edit more information
@knowledge_base_blueprint.route('/client/<int:client_id>/edit_more_info/<int:info_id>', methods=['POST'])
def edit_more_info(client_id, info_id):
    more_info = MoreInformation.query.get_or_404(info_id)
    more_info.info_type = request.form.get('info_type')
    more_info.link = request.form.get('link')
    more_info.rules = request.form.get('rules')

    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to delete more information
@knowledge_base_blueprint.route('/client/<int:client_id>/delete_more_info/<int:info_id>', methods=['POST'])
def delete_more_info(client_id, info_id):
    more_info = MoreInformation.query.get_or_404(info_id)
    db.session.delete(more_info)
    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to add a case study
@knowledge_base_blueprint.route('/client/<int:client_id>/add_case_study', methods=['POST'])
def add_case_study(client_id):
    title = request.form.get('title')
    link = request.form.get('link')
    rules = request.form.get('rules')

    case_study = CaseStudy(client_id=client_id, title=title, link=link, rules=rules)
    db.session.add(case_study)
    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to edit a case study
@knowledge_base_blueprint.route('/client/<int:client_id>/edit_case_study/<int:study_id>', methods=['POST'])
def edit_case_study(client_id, study_id):
    case_study = CaseStudy.query.get_or_404(study_id)
    case_study.title = request.form.get('title')
    case_study.link = request.form.get('link')
    case_study.rules = request.form.get('rules')

    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to delete a case study
@knowledge_base_blueprint.route('/client/<int:client_id>/delete_case_study/<int:study_id>', methods=['POST'])
def delete_case_study(client_id, study_id):
    case_study = CaseStudy.query.get_or_404(study_id)
    db.session.delete(case_study)
    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to add a problem/solution
@knowledge_base_blueprint.route('/client/<int:client_id>/add_problem_solution', methods=['POST'])
def add_problem_solution(client_id):
    problem = request.form.get('problem')
    solution = request.form.get('solution')

    problem_solution = ProblemSolution(client_id=client_id, problem=problem, solution=solution)
    db.session.add(problem_solution)
    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to edit a problem/solution
@knowledge_base_blueprint.route('/client/<int:client_id>/edit_problem_solution/<int:ps_id>', methods=['POST'])
def edit_problem_solution(client_id, ps_id):
    problem_solution = ProblemSolution.query.get_or_404(ps_id)
    problem_solution.problem = request.form.get('problem')
    problem_solution.solution = request.form.get('solution')

    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to delete a problem/solution
@knowledge_base_blueprint.route('/client/<int:client_id>/delete_problem_solution/<int:ps_id>', methods=['POST'])
def delete_problem_solution(client_id, ps_id):
    problem_solution = ProblemSolution.query.get_or_404(ps_id)
    db.session.delete(problem_solution)
    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to add a noteworthy client
@knowledge_base_blueprint.route('/client/<int:client_id>/add_noteworthy_client', methods=['POST'])
def add_noteworthy_client(client_id):
    name = request.form.get('name')
    website = request.form.get('website')
    kpis = request.form.get('kpis')

    noteworthy_client = NoteworthyClient(client_id=client_id, name=name, website=website, kpis=kpis)
    db.session.add(noteworthy_client)
    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to edit a noteworthy client
@knowledge_base_blueprint.route('/client/<int:client_id>/edit_noteworthy_client/<int:nc_id>', methods=['POST'])
def edit_noteworthy_client(client_id, nc_id):
    noteworthy_client = NoteworthyClient.query.get_or_404(nc_id)
    noteworthy_client.name = request.form.get('name')
    noteworthy_client.website = request.form.get('website')
    noteworthy_client.kpis = request.form.get('kpis')

    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to delete a noteworthy client
@knowledge_base_blueprint.route('/client/<int:client_id>/delete_noteworthy_client/<int:nc_id>', methods=['POST'])
def delete_noteworthy_client(client_id, nc_id):
    noteworthy_client = NoteworthyClient.query.get_or_404(nc_id)
    db.session.delete(noteworthy_client)
    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to add a feature
@knowledge_base_blueprint.route('/client/<int:client_id>/add_feature', methods=['POST'])
def add_feature(client_id):
    title = request.form.get('title')
    description = request.form.get('description')
    link = request.form.get('link')

    feature = Feature(client_id=client_id, title=title, description=description, link=link)
    db.session.add(feature)
    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to edit a feature
@knowledge_base_blueprint.route('/client/<int:client_id>/edit_feature/<int:feature_id>', methods=['POST'])
def edit_feature(client_id, feature_id):
    feature = Feature.query.get_or_404(feature_id)
    feature.title = request.form.get('title')
    feature.description = request.form.get('description')
    feature.link = request.form.get('link')

    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))

# Route to delete a feature
@knowledge_base_blueprint.route('/client/<int:client_id>/delete_feature/<int:feature_id>', methods=['POST'])
def delete_feature(client_id, feature_id):
    feature = Feature.query.get_or_404(feature_id)
    db.session.delete(feature)
    db.session.commit()

    return redirect(url_for('knowledge_base.client_knowledge_base', client_id=client_id))