from config import Config
from helpers.date_helper import verify_date_range
from helpers.request_helper import request_url
from helpers.consts import *
from services.country_service import *

additional_query_parameter = '&targets=companies,officers,documents,publications&lang=fr'

def get_search_query(request):
    country = request.form.get(COUNTRY).upper()
    in_activity = request.form.get(IN_ACTIVITY, 'true')
    region_code = request.form.getlist(REGION)
    postal_code = request.form.getlist(POSTAL_CODE)
    legal_form = request.form.getlist(LEGAL_FORM)
    legal_situation = request.form.getlist(LEGAL_SITUATION)
    activities = request.form.getlist(ACTIVITY)
    min_ca = request.form.get(MIN_CA, 0)
    max_ca = request.form.get(MAX_CA, 0)
    min_res = request.form.get(MIN_RES, 0)
    max_res = request.form.get(MAX_RES, 0)
    min_eff = request.form.get(MIN_EFF, 0)
    max_eff = request.form.get(MAX_EFF, 0)
    min_cap = request.form.get(MIN_CAP, 0)
    max_cap = request.form.get(MAX_CAP, 0)
    min_age = request.form.get(MIN_AGE, 0)
    max_age = request.form.get(MAX_AGE, 0)
    creation_date_start_str = request.form.get(CREATION_DATE_START, '')
    creation_date_end_str = request.form.get(CREATION_DATE_END, '')

    query = f'{get_query_parameter_dictionary(country)[COUNTRY]}={country}'
    if in_activity == 'on':
        query = f'{query}&{get_query_parameter_dictionary(country)[IN_ACTIVITY]}=active'
    if postal_code:
        query = f'{query}&{get_query_parameter_dictionary(country)[POSTAL_CODE]}={",".join(postal_code)}'
    if region_code:
        query = f'{query}&{get_query_parameter_dictionary(country)[REGION]}={",".join(region_code)}'
    if legal_form:
        query = f'{query}&{get_query_parameter_dictionary(country)[LEGAL_FORM]}={",".join(legal_form)}'
    if legal_situation:
        query = f'{query}&{get_query_parameter_dictionary(country)[LEGAL_SITUATION]}={",".join(legal_situation)}'
    if activities:
        query = f'{query}&{get_query_parameter_dictionary(country)[ACTIVITY]}={",".join(activities)}'

    if creation_date_end_str != '':
        if creation_date_start_str == '':
            creation_date_start_str = creation_date_end_str
        verify_date_range(creation_date_start_str, creation_date_end_str)
        query = f'{query}&{get_query_parameter_dictionary(country)[CREATION_DATE_START]}={creation_date_start_str}&{get_query_parameter_dictionary(country)[CREATION_DATE_END]}={creation_date_end_str}'
    elif creation_date_start_str != '':
        if creation_date_end_str == '':
            creation_date_end_str = creation_date_start_str
        verify_date_range(creation_date_start_str, creation_date_end_str)
        query = f'{query}&{get_query_parameter_dictionary(country)[CREATION_DATE_START]}={creation_date_start_str}&{get_query_parameter_dictionary(country)[CREATION_DATE_END]}={creation_date_end_str}'

    query = set_query_for_number(max_ca, min_ca, MIN_CA, MAX_CA, 0, 100000000000, country, query, lambda x: x)
    query = set_query_for_number(max_res, min_res, MIN_RES, MAX_RES, 0, 100000000000, country, query, lambda x: x)
    query = set_query_for_number(max_cap, min_cap, MIN_CAP, MAX_CAP, 0, 100000000000, country, query, lambda x: x)
    query = set_query_for_number(max_age, min_age, MIN_AGE, MAX_AGE, 0, 1000, country, query, lambda x: x)
    query = set_query_for_number(max_eff, min_eff, MIN_EFF, MAX_EFF, 1, 9, country, query, get_workforce_number)

    query = f'{query}{additional_query_parameter}'

    return query

def set_query_for_number(max_value, min_value, min_const, max_const, min_number, max_number, country, query, modify_value_func):
    new_query = query
    if max_value != '' and max_value != 0:
        if min_value == '':
            min_value = min_number
        new_query = f'{new_query}&{get_query_parameter_dictionary(country)[min_const]}={modify_value_func(min_value)}&{get_query_parameter_dictionary(country)[max_const]}={modify_value_func(max_value)}'
    elif min_value != '' and min_value != 0:
        if max_value == '' or max_value == 0:
            max_value = max_number
        new_query = f'{new_query}&{get_query_parameter_dictionary(country)[min_const]}={modify_value_func(min_value)}&{get_query_parameter_dictionary(country)[max_const]}={modify_value_func(max_value)}'
    return new_query

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
    pappers_query = pappers_query.replace(additional_query_parameter, '')
    criterias = []
    for criteria in pappers_query.split('&'):
        splitted = criteria.split('=')
        key = splitted[0]
        value = splitted[1]
        if get_criteria_dictionary(country).get(key):
            criterias.append({'key': get_criteria_dictionary(country)[key], 'value': get_value(key, value, country)})
        else:
            criterias.append({'key': key, 'value': get_value(key, value, country)})

    return criterias

def get_value(key, value, country):
    if key == "country_code":
        return Config.COUNTRIES.get(value)
    if key == "postal_code":
        return find_postal_code(country, value)
    if key == "region":
        return find_region_code(country, value)
    if key == "local_legal_form_code":
        return find_legal_forms(country, value)
    if key == "legal_situation_code":
        return find_legal_situations(country, value)
    if key == "local_activity_code":
        return find_activities(country, value)
    else:
        return value

def search_companies_request(search_request, country):
    search_request = f'{search_request}&api_token={get_pappers_api_search_key(country)}'
    url = f'{get_pappers_api_search_url(country)}?{search_request}'
    return request_url(url)

def get_number_of_companies(country, search_request):
    response = search_companies_request(search_request, country)
    pappers_information = []
    number_of_companies = 0
    if response:
        results = response.json()
        number_of_companies = results.get(get_response_dictionary(country)[TOTAL])
        i = 0
        for data in results.get(get_response_dictionary(country)[RESULTS], []):
            if i == 5:
                break
            pappers_information.append(create_pappers_info(data, country))
            i = i + 1
    return {'number': number_of_companies, 'companies': pappers_information}


def get_officer_data(company_number, country):
    search_request = f'api_token={get_pappers_api_company_key(country)}&{get_query_parameter_dictionary(country)[COUNTRY]}={country}&{get_query_parameter_dictionary(country)[COMPANY_NUMBER]}={company_number}&fields=officers,ubos,financials,documents,certificates,publications,establishments,contacts'
    url = f'{get_pappers_api_company_url(country)}?{search_request}'
    return request_url(url)

def search_companies(country: str, search_request: str, nb_company: int, add_officer_info: bool):
    nb_company_per_page = 20
    pappers_information = []

    current_nb = 1
    nb_request = int(nb_company) / nb_company_per_page
    if nb_request != 1 and nb_request % 2 != 0:
        nb_request = nb_request + 1

    for i in range(int(nb_request)):
        if current_nb > nb_company:
            break

        page_search_request = f'{search_request}&page={i + 1}&par_page=20'
        response = search_companies_request(page_search_request, country)

        if response:
            results = response.json()
            for data in results.get(get_response_dictionary(country)[RESULTS], []):
                if current_nb > nb_company:
                    break

                pappers_info = create_pappers_info(data, country)

                if add_officer_info:
                    officer_data_response = get_officer_data(data.get(get_response_dictionary(country)[COMPANY_NUMBER], ''), country)
                    if officer_data_response:
                        officer_data = officer_data_response.json()
                        pappers_info.add_officer_info(officer_data)

                pappers_information.append(pappers_info)
                current_nb = current_nb + 1

    return pappers_information