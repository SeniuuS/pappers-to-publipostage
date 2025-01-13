from models.belgium import Belgium

belgium = Belgium()

countries = {'FR': None, 'BE': belgium, 'CH': None}

def get_legal_situations(country):
    return countries[country].legal_situations

def get_legal_forms(country):
    return countries[country].legal_forms

def get_postal_codes(country):
    return countries[country].postal_codes

def find_postal_code(country, search_postal_code):
    postal_codes = get_postal_codes(country)
    for postal_code in postal_codes:
        if postal_code["code_postal"] == search_postal_code:
            return postal_code
    return search_postal_code

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