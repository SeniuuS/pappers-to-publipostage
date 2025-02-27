import json

from helpers.consts import *

class PapperForm():
    def __init__(self, country, request):
        self.country = country
        self.in_activity = 'false'
        self.postal_code = ''
        self.legal_form = []
        self.legal_situation = []
        self.activities = []
        self.activity_group = []
        self.region = []
        self.min_ca = None
        self.max_ca = None
        self.min_res = None
        self.max_res = None
        self.min_eff = None
        self.max_eff = None
        self.min_cap = None
        self.max_cap = None
        self.min_age = None
        self.max_age = None
        self.creation_date_start_str = ''
        self.creation_date_end_str = ''

        if request is not None:
            self.set_form(request)

    def set_form(self, request):
        self.country = request.form.get(COUNTRY).upper()
        self.in_activity = request.form.get(IN_ACTIVITY, 'false')
        self.postal_code = request.form.getlist(POSTAL_CODE)
        self.legal_form = request.form.getlist(LEGAL_FORM)
        self.legal_situation = request.form.getlist(LEGAL_SITUATION)
        self.activities = request.form.getlist(ACTIVITY)
        self.activity_group = request.form.getlist(ACTIVITY_GROUP)
        self.region = request.form.getlist(REGION)
        self.min_ca = request.form.get(MIN_CA, 0)
        self.max_ca = request.form.get(MAX_CA, 0)
        self.min_res = request.form.get(MIN_RES, 0)
        self.max_res = request.form.get(MAX_RES, 0)
        self.min_eff = request.form.get(MIN_EFF, 0)
        self.max_eff = request.form.get(MAX_EFF, 0)
        self.min_cap = request.form.get(MIN_CAP, 0)
        self.max_cap = request.form.get(MAX_CAP, 0)
        self.min_age = request.form.get(MIN_AGE, 0)
        self.max_age = request.form.get(MAX_AGE, 0)
        self.creation_date_start_str = request.form.get(CREATION_DATE_START, '')
        self.creation_date_end_str = request.form.get(CREATION_DATE_END, '')

    def to_json(self):
        return json.dumps(self, default=lambda o: o.__dict__)

    def load_json(self, json_form):
        self.country = json_form['country']
        self.in_activity = json_form['in_activity']
        self.postal_code = json_form['postal_code']
        self.legal_form = json_form['legal_form']
        self.legal_situation = json_form['legal_situation']
        self.activities = json_form['activities']
        self.activity_group = json_form['activity_group']
        self.region = json_form['region']
        self.min_ca = json_form['min_ca']
        self.max_ca = json_form['max_ca']
        self.min_res = json_form['min_res']
        self.max_res = json_form['max_res']
        self.min_eff = json_form['min_eff']
        self.max_eff = json_form['max_eff']
        self.min_cap = json_form['min_cap']
        self.max_cap = json_form['max_cap']
        self.min_age = json_form['min_age']
        self.max_age = json_form['max_age']
        self.creation_date_start_str = json_form['creation_date_start_str']
        self.creation_date_end_str = json_form['creation_date_end_str']