import requests
from config import Config
from services.country_service import *
from models.pappers_info import PappersInfo

criteria_dictionnary = {'status': 'Active', 'postal_code': 'Code Postal', 'local_legal_form_code': 'Forme juridique', 'legal_situation_code': 'Situation juridique',
                        'turnover_min': 'Chiffre d\'affaire minimum', 'turnover_max': 'Chiffre d\'affaire maximum',
                        'net_income_min': 'Résultat minimum', 'net_income_max': 'Résultat maximum',
                        'workforce_range_min': 'Effectif minimum', 'workforce_range_max': 'Effectif maximum'}

def get_search_query(request):
    country = request.form.get('country').upper()
    in_activity = request.form.get('inActivity', 'true')
    postal_code = request.form.get('postalCode', '').upper()
    legal_form = request.form.getlist('legalForm')
    legal_situation = request.form.getlist('legalSituation')
    min_ca = request.form.get('minCA', 0)
    max_ca = request.form.get('maxCA', 0)
    min_res = request.form.get('minRES', 0)
    max_res = request.form.get('maxRES', 0)
    min_eff = request.form.get('minEff', 0)
    max_eff = request.form.get('maxEff', 0)

    query = f'country_code={country}'
    if in_activity == 'on':
        query = f'{query}&status=active'
    if postal_code != '':
        query = f'{query}&postal_code={postal_code}'
    if legal_form:
        query = f'{query}&local_legal_form_code={",".join(legal_form)}'
    if legal_situation:
        query = f'{query}&legal_situation_code={",".join(legal_situation)}'

    if max_ca != '' and max_ca != 0:
        if min_ca == '':
            min_ca = 0
        query = f'{query}&turnover_min={min_ca}&turnover_max={max_ca}'
    elif min_ca != '' and min_ca != 0:
        if max_ca == '' or max_ca == 0:
            max_ca = 100000000000
        query = f'{query}&turnover_min={min_ca}&turnover_max={max_ca}'

    if max_res != '' and max_res != 0:
        if min_res == '':
            min_res = 0
        query = f'{query}&net_income_min={min_res}&net_income_max={max_res}'
    elif min_res != '' and min_res != 0:
        if max_res == '' or max_res == 0:
            max_res = 100000000000
        query = f'{query}&net_income_min={min_res}&net_income_max={max_res}'

    if max_eff != '' and max_eff != 0:
        if min_eff == '':
            min_eff = 1
        query = f'{query}&workforce_range_min={get_workforce_number(min_eff)}&workforce_range_max={get_workforce_number(max_eff)}'
    elif min_eff != '' and min_eff != 0:
        if max_eff == '' or max_eff == 0:
            max_eff = 9
        query = f'{query}&workforce_range_min={get_workforce_number(min_eff)}&workforce_range_max={max_eff}'

    query = f'{query}&targets=companies,officers,documents,publications&lang=fr'

    return query

def get_workforce_number(eff):
    workforce = int(eff)
    if workforce < 5:
        return 1
    if workforce < 10:
        return 2
    elif workforce < 20:
        return 3
    elif workforce < 50:
        return 4
    elif workforce < 100:
        return 5
    elif workforce < 200:
        return 6
    elif workforce < 500:
        return 7
    elif workforce < 1000:
        return 8
    elif workforce < 500000:
        return 9

def get_criterias(pappers_query, country):
    criterias = []
    for criteria in pappers_query.split('&'):
        splitted = criteria.split('=')
        key = splitted[0]
        value = splitted[1]
        if criteria_dictionnary.get(key):
            criterias.append({'key': criteria_dictionnary[key], 'value': get_value(key, value, country)})
        else:
            criterias.append({'key': key, 'value': get_value(key, value, country)})

    return criterias

def get_value(key, value, country):
    if key == "country_code":
        return Config.COUNTRIES.get(value)
    if key == "postal_code":
        return find_postal_code(country, value)
    if key == "local_legal_form_code":
        return find_legal_forms(country, value)
    if key == "legal_situation_code":
        return find_legal_situations(country, value)
    else:
        return value

def search_companies_request(search_request):
    search_request = f'{search_request}&api_token={Config.PAPPERS_API_KEY}'

    response = requests.get(
        f'{Config.PAPPERS_API_SEARCH_URL}?{search_request}'
    )

    if response.status_code == 200:
        return response
    return None

def get_number_of_companies(search_request):
    response = search_companies_request(search_request)
    if response:
        results = response.json()
        return results.get("total")
    return 0

def search_companies(country, search_request, nb_company):
    nb_company_per_page = 20
    pappers_information = []

    nb_request = int(nb_company) / nb_company_per_page
    if nb_request % 2 != 0:
        nb_request = int(nb_request) + 1

    for i in range(nb_request):
        page_search_request = f'{search_request}&page={i + 1}&par_page=20'
        response = search_companies_request(page_search_request)

        if response:
            results = response.json()
            for data in results.get('results', []):
                nom_societe = data.get('name', '')
                head_office = data.get('head_office', {})
                country_found = head_office.get('country', '')

                if country_found is None:
                    country_found = Config.COUNTRIES[country]

                adresse = f"{head_office.get('address_line_1', '')} {head_office.get('postal_code', '')} {head_office.get('city', '')} {country_found}"
                nom_dirigeant = (
                    f"{data.get('officers', [{}])[0].get('last_name', '')} {data.get('officers', [{}])[0].get('first_name', '')}"
                    if data.get('officers') else ''
                )
                email = data.get('emails', [])[0] if data.get('emails') else ''
                telephone = data.get('telephones', [])[0] if data.get('telephones') else ''
                company_number = data.get('company_number', '')

                pappers_information.append(PappersInfo(nom_societe, adresse, nom_dirigeant, email, telephone, company_number))

    return pappers_information