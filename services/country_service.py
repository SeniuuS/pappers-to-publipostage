from models.belgium import Belgium
from models.france import France
from models.pappers_info import PappersInfo
from models.pappers_info_fr import PappersInfoFR

belgium = Belgium()
france = France()

countries = {'FR': france, 'BE': belgium, 'CH': None}

def create_pappers_info(data, country):
    if country == 'FR':
        return PappersInfoFR(data, country)
    return PappersInfo(data, country)

def get_legal_situations(country):
    return countries[country].legal_situations

def get_legal_forms(country):
    return countries[country].legal_forms

def get_postal_codes(country):
    return countries[country].postal_codes

def get_region_codes(country):
    return countries[country].region_codes

def get_activities(country):
    return countries[country].activities

def get_activities_group(country):
    return countries[country].activities_group

def get_criteria_dictionary(country):
    return countries[country].criteria_dictionnary

def get_query_parameter_dictionary(country):
    return countries[country].query_parameter_dictionary

def get_response_dictionary(country):
    return countries[country].response_dictionary

def get_pappers_api_search_url(country):
    return countries[country].pappers_api_search_url

def get_pappers_api_company_url(country):
    return countries[country].pappers_api_company_url

def get_pappers_api_search_key(country):
    return countries[country].pappers_api_search_key

def get_pappers_api_company_key(country):
    return countries[country].pappers_api_company_key

def get_activities_naf_from_group(country, activity_group):
    found_activities = []
    activities_group = get_activities_group(country)
    for activity in activity_group:
        found_activities.extend(activities_group[activity])
    return found_activities

def find_postal_code(country, search_postal_code):
    postal_codes = get_postal_codes(country)
    for postal_code in postal_codes:
        if postal_code["code_postal"] == search_postal_code:
            return f'{postal_code["code_postal"]} - {postal_code["commune"]}'
    return search_postal_code

def find_region_code(country, search_region_code):
    region_codes = get_region_codes(country)
    for region_code in region_codes:
        if region_code["code"] == search_region_code:
            return f'{region_code["name"]}'
    return search_region_code

def find_legal_situations(country, search_legal_situations):
    found_legal_situations = ""
    legal_situations = get_legal_situations(country)
    for search_legal_situation in search_legal_situations.split(','):
        for legal_situation in legal_situations:
            if str(legal_situation["c"]) == search_legal_situation:
                found_legal_situations = f'{found_legal_situations}{legal_situation["n"]},'
    if found_legal_situations == "":
        return search_legal_situations
    else:
        found_legal_situations = found_legal_situations[:-1]
    return found_legal_situations

def find_legal_forms(country, search_legal_forms):
    found_legal_forms = ""
    legal_forms = get_legal_forms(country)
    for search_legal_form in search_legal_forms.split(','):
        for legal_form in legal_forms:
            if str(legal_form["c"]) == search_legal_form:
                found_legal_forms = f'{found_legal_forms}{legal_form["n"]},'
    if found_legal_forms == "":
        return search_legal_forms
    else:
        found_legal_forms = found_legal_forms[:-1]
    return found_legal_forms

def find_activities(country, search_activities):
    found_activities = ""
    activities = get_activities(country)
    for search_activity in search_activities.split(','):
        for activity in activities:
            if activity["code"] == search_activity:
                found_activities = f'{found_activities}{activity["code"]}-{activity["libelle"]},'
    if found_activities == "":
        return search_activities
    else:
        found_activities = found_activities[:-1]
    return found_activities