import json

from flask import session

from models.pappers_form import PapperForm


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