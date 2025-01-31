import json

from models.pappers_form import PapperForm
from . import bp
from flask import render_template, request, send_file, jsonify, redirect, url_for, session

from services.pappers_service import get_search_query, search_companies, get_number_of_companies, get_criterias
from services.excel_service import create_excel_file
from services.country_service import get_activities, get_legal_forms, get_legal_situations, get_postal_codes
from services.authentication_service import can_do_detailed_export

@bp.route('/', methods=['GET'])
def home():
    country = request.args.get('country', 'BE').upper()
    return redirect(url_for('main.index', country=country))

@bp.route('/index', methods=['GET'])
def index():
    return index_with_error(None)

@bp.route('/reset', methods=['POST'])
def reset():
    country = request.form.get('country').upper()
    initialize_form_session(country, None)
    return redirect(url_for('main.index', country=country))

def initialize_form_session(country, req):
    session['current_form'] = PapperForm(country, req).to_json()

def get_form_session():
    json_form = json.loads(session['current_form'])
    current_form = PapperForm(None, None)
    current_form.load_json(json_form)
    return current_form

def set_form_session(country, req):
    if req is not None:
        initialize_form_session(country, req)
    if 'current_form' not in session:
        initialize_form_session(country, req)
    current_form = get_form_session()
    if current_form.country != country:
        initialize_form_session(country, req)
    current_form = get_form_session()
    return current_form

def index_with_error(error: Exception):
    country = request.args.get('country', 'BE').upper()

    current_form = set_form_session(country, None)

    legal_situations = get_legal_situations(country)
    legal_forms = get_legal_forms(country)
    activities = get_activities(country)

    if error:
        return render_template('index.jinja2', country=country, legal_situations=legal_situations, legal_forms=legal_forms, activities=activities, form=current_form, error=str(error))
    return render_template('index.jinja2', country=country, legal_situations=legal_situations, legal_forms=legal_forms, activities=activities, form=current_form)

@bp.route('/search', methods=['POST'])
def search():
    country = request.form.get('country').upper()

    try:
        set_form_session(country, request)
        pappers_query = get_search_query(request)
        criterias = get_criterias(pappers_query, country)
        companies_found = get_number_of_companies(country, pappers_query)
        nb_export_max = 200
        if nb_export_max > companies_found['number']:
            nb_export_max = companies_found['number']
        return render_template('download.html', country=country, nb_export_max=nb_export_max, nb_company=companies_found['number'], companies=companies_found['companies'], criterias=criterias, query=pappers_query)
    except Exception as e:
        return index_with_error(e)


@bp.route('/download', methods=['POST'])
def download():
    country = request.form.get('country').upper()
    pappers_query = request.form.get('query')
    nb_export = int(request.form.get('nbExport'))
    add_officer_info = request.form.get('detailedCheckBox')
    detailed_export_key = request.form.get('detailedExportKey')
    if nb_export == 0:
        return redirect(url_for('main.index'))
    if nb_export > 200:
        nb_export = 200

    pappers_information = search_companies(country, pappers_query, nb_export, can_do_detailed_export(add_officer_info, detailed_export_key))
    file_path = create_excel_file(get_criterias(pappers_query, country), pappers_information)
    return send_file(file_path, as_attachment=True)

@bp.route("/autocompletePostalCode", methods=["GET"])
def auto_complete_postal_code():
    country = request.args.get('countryCode').upper()
    postal_codes = get_postal_codes(country)
    query = request.args.get("q", "").lower()
    results = [
        {'id': entry['code_postal'], 'name': f"{entry['code_postal']} - {entry['commune']}"}
        for entry in postal_codes
        if query in entry['commune'].lower() or query in entry['code_postal']
    ]
    return jsonify(results)