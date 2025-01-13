from . import bp
from flask import render_template, request, send_file, jsonify
from services.pappers_service import get_search_query, search_companies, get_number_of_companies, get_criterias
from services.excel_service import create_excel_file
from services.country_service import *

@bp.route('/', methods=['GET'])
def index():
    country = request.args.get('country', 'BE').upper()
    legal_situations = get_legal_situations(country)
    legal_forms = get_legal_situations(country)

    return render_template('index.html', country=country, legal_situations=legal_situations, legal_forms=legal_forms)

@bp.route('/search', methods=['POST'])
def search():
    country = request.form.get('country').upper()

    pappers_query = get_search_query(request)
    nb_company = get_number_of_companies(pappers_query)
    return render_template('download.html', country=country, nb_company=nb_company, query=pappers_query)

@bp.route('/download', methods=['POST'])
def download():
    country = request.form.get('country').upper()
    pappers_query = request.form.get('query')
    nb_company = request.form.get('nb_company')

    pappers_information = search_companies(country, pappers_query, nb_company)
    file_path = create_excel_file(get_criterias(pappers_query, country), pappers_information)
    return send_file(file_path, as_attachment=True)

@bp.route("/autocompletePostalCode", methods=["GET"])
def autocompletePostalCode():
    country = request.form.get('country').upper()
    postal_codes = get_postal_codes(country)
    query = request.args.get("q", "").lower()
    results = [
        {'id': entry['code_postal'], 'name': f"{entry['code_postal']} - {entry['commune']}"}
        for entry in postal_codes
        if query in entry['commune'].lower() or query in entry['code_postal']
    ]
    return jsonify(results)