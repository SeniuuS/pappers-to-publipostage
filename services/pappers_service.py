import logging
import requests
from config import Config
from helpers.date_helper import verify_date_range
from services.country_service import *
from models.pappers_info import PappersInfo

criteria_dictionnary = {'status': 'Active', 'postal_code': 'Code Postal', 'local_legal_form_code': 'Forme juridique', 'legal_situation_code': 'Situation juridique',
                        'local_activity_code': 'Activités', 'turnover_min': 'Chiffre d\'affaire minimum', 'turnover_max': 'Chiffre d\'affaire maximum',
                        'net_income_min': 'Résultat minimum', 'net_income_max': 'Résultat maximum',
                        'workforce_range_min': 'Effectif minimum', 'workforce_range_max': 'Effectif maximum',
                        'date_of_creation_min': 'Date de création (min)', 'date_of_creation_max': 'Date de création (max)',
                        'country_code': 'Pays'}

def get_search_query(request):
    country = request.form.get('country').upper()
    in_activity = request.form.get('inActivity', 'true')
    postal_code = request.form.get('postalCode', '').upper()
    legal_form = request.form.getlist('legalForm')
    legal_situation = request.form.getlist('legalSituation')
    activities = request.form.getlist('activity')
    min_ca = request.form.get('minCA', 0)
    max_ca = request.form.get('maxCA', 0)
    min_res = request.form.get('minRES', 0)
    max_res = request.form.get('maxRES', 0)
    min_eff = request.form.get('minEff', 0)
    max_eff = request.form.get('maxEff', 0)
    creation_date_start_str = request.form.get('creationDateStart', '')
    creation_date_end_str = request.form.get('creationDateEnd', '')

    query = f'country_code={country}'
    if in_activity == 'on':
        query = f'{query}&status=active'
    if postal_code != '':
        query = f'{query}&postal_code={postal_code}'
    if legal_form:
        query = f'{query}&local_legal_form_code={",".join(legal_form)}'
    if legal_situation:
        query = f'{query}&legal_situation_code={",".join(legal_situation)}'
    if activities:
        query = f'{query}&local_activity_code={",".join(activities)}'

    if creation_date_end_str != '':
        if creation_date_start_str == '':
            creation_date_start_str = creation_date_end_str
        verify_date_range(creation_date_start_str, creation_date_end_str)
        query = f'{query}&date_of_creation_min={creation_date_start_str}&date_of_creation_max={creation_date_end_str}'
    elif creation_date_start_str != '':
        if creation_date_end_str == '':
            creation_date_end_str = creation_date_start_str
        verify_date_range(creation_date_start_str, creation_date_end_str)
        query = f'{query}&date_of_creation_min={creation_date_start_str}&date_of_creation_max={creation_date_end_str}'

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
    if key == "local_activity_code":
        return find_activities(country, value)
    else:
        return value

def search_companies_request(search_request):
    search_request = f'{search_request}&api_token={Config.PAPPERS_API_KEY}'

    url = f'{Config.PAPPERS_API_SEARCH_URL}?{search_request}'

    logging.info(f"Requesting {url}")

    response = requests.get(url)

    if response.status_code == 200:
        logging.info(f"Request {url} successful : 200")
        return response
    logging.warning(f"Error requesting {url} : {response.status_code}")
    return None

def get_number_of_companies(country, search_request):
    response = search_companies_request(search_request)
    pappers_information = []
    number_of_companies = 0
    if response:
        results = response.json()
        number_of_companies = results.get("total")
        i = 0
        for data in results.get('results', []):
            if i == 5:
                break
            pappers_information.append(PappersInfo(data, country))
            i = i + 1
    return {'number': number_of_companies, 'companies': pappers_information}

def search_companies(country, search_request, nb_company):
    nb_company_per_page = 20
    pappers_information = []

    nb_request = int(nb_company) / nb_company_per_page
    if nb_request != 1 and nb_request % 2 != 0:
        nb_request = nb_request + 1

    for i in range(int(nb_request)):
        page_search_request = f'{search_request}&page={i + 1}&par_page=20'
        response = search_companies_request(page_search_request)

        if response:
            results = response.json()
            for data in results.get('results', []):
                pappers_information.append(PappersInfo(data, country))

    return pappers_information