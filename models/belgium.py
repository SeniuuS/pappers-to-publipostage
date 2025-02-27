import csv
import os

import pandas as pd

from config import Config
from helpers.json_helper import read_file_json
from helpers.consts import *

CITY_COLUMN = 'Municipality name (French)'
POSTAL_CODE_COLUMN = 'Postal Code'
REGION_CODE_COLUMN = 'Région code'

class Belgium:
    postal_codes_file = os.path.join('sources', 'postal-codes-belgium.csv')
    legal_form_file = os.path.join('sources', 'forme-juridique-belgium.json')
    legal_situation_file = os.path.join('sources', 'situation-juridique-belgium.json')
    activities_file = os.path.join('sources', 'TU_COM_NACEBEL_2008.xlsx')

    criteria_dictionnary = {'status': 'Active', 'postal_code': 'Code Postal',
                            'local_legal_form_code': 'Forme juridique', 'legal_situation_code': 'Situation juridique',
                            'local_activity_code': 'Activités', 'turnover_min': 'Chiffre d\'affaire minimum',
                            'turnover_max': 'Chiffre d\'affaire maximum',
                            'net_income_min': 'Résultat minimum', 'net_income_max': 'Résultat maximum',
                            'capital_min': 'Capital minimum', 'capital_max': 'Capital maximum',
                            'workforce_range_min': 'Effectif minimum', 'workforce_range_max': 'Effectif maximum',
                            'date_of_creation_min': 'Date de création (min)',
                            'date_of_creation_max': 'Date de création (max)',
                            'country_code': 'Pays'}

    query_parameter_dictionary = {IN_ACTIVITY: 'status', POSTAL_CODE: 'postal_code', LEGAL_FORM: 'local_legal_form_code',
                              LEGAL_SITUATION: 'legal_situation_code', ACTIVITY: 'local_activity_code',
                              MIN_CA: 'turnover_min', MAX_CA: 'turnover_max', MIN_RES: 'net_income_min',
                              MAX_RES: 'net_income_max', MIN_EFF: 'workforce_range_min', MAX_EFF: 'workforce_range_max',
                              MIN_CAP: 'capital_min', MAX_CAP: 'capital_max',
                              CREATION_DATE_START: 'date_of_creation_min', CREATION_DATE_END: 'date_of_creation_max',
                              COUNTRY: 'country_code', COMPANY_NUMBER: 'company_number'}

    response_dictionary = {RESULTS: 'results', COMPANY_NUMBER: 'company_number', TOTAL: 'total'}

    pappers_api_search_url = Config.PAPPERS_API_SEARCH_URL
    pappers_api_company_url = Config.PAPPERS_API_COMPANY_URL
    pappers_api_search_key = Config.PAPPERS_API_KEY
    pappers_api_company_key = Config.PAPPERS_API_COMPANY_PERSO_KEY

    postal_codes = []
    region_codes = []
    legal_forms = []
    legal_situations = []
    activities = []

    def __init__(self):
        self.init_postal_codes()
        self.init_legal_form()
        self.init_legal_situation()
        self.init_activities()

    def init_postal_codes(self):
        with open(self.postal_codes_file, mode='r', encoding='utf-8') as csv_file:
            lecteur_csv = csv.DictReader(csv_file, delimiter=';')
            for ligne in lecteur_csv:
                if ligne[CITY_COLUMN].strip():
                    self.postal_codes.append({"code_postal": ligne[POSTAL_CODE_COLUMN], "commune": ligne[CITY_COLUMN]})
        self.postal_codes = sorted(self.postal_codes, key=lambda item: int(item['code_postal']))

    def init_activities(self):
        df = pd.read_excel(self.activities_file)
        level_5_codes = df[df['LVL_NACEBEL'] == 5]
        self.activities = [{'code': str(row['CD_NACEBEL']), 'libelle': row['TX_NACEBEL_FR']} for _, row in level_5_codes.iterrows()]

    def init_legal_form(self):
        self.legal_forms = read_file_json(self.legal_form_file)

    def init_legal_situation(self):
        self.legal_situations = read_file_json(self.legal_situation_file)