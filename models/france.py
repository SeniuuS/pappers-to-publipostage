import csv
import os

import pandas as pd

from config import Config
from helpers.consts import *

CITY_COLUMN = 'Libelle'
POSTAL_CODE_COLUMN = 'Code_Postal'
COMMUNE_CODE_COLUMN = 'Code_commune_INSEE'

class France:
    region_codes_file = os.path.join('sources', 'regions-france.csv')
    postal_codes_file = os.path.join('sources', 'postal-codes-france.csv')
    legal_form_file = os.path.join('sources', 'cj_septembre_2022.xls')
    activities_file = os.path.join('sources', 'int_courts_naf_rev_2.xls')

    criteria_dictionnary = {'status': 'Active', 'code_postal': 'Code Postal',
                            'categorie_juridique': 'Forme juridique',
                            'code_naf_elargi': 'Activités', 'chiffre_affaires_min': 'Chiffre d\'affaire minimum',
                            'chiffre_affaires_max': 'Chiffre d\'affaire maximum',
                            'resultat_min': 'Résultat minimum', 'resultat_max': 'Résultat maximum',
                            'capital_min': 'Capital minimum', 'capital_max': 'Capital maximum',
                            'age_dirigeant_min': 'Age dirigeant minimum', 'age_dirigeant_max': 'Age dirigeant maximum',
                            'tranche_effectif_min': 'Effectif minimum', 'tranche_effectif_max': 'Effectif maximum', 'region': 'Région',
                            'date_creation_min': 'Date de création (min)',
                            'date_creation_max': 'Date de création (max)'}

    query_parameter_dictionary = {IN_ACTIVITY: 'status', POSTAL_CODE: 'code_postal', LEGAL_FORM: 'categorie_juridique',
                              LEGAL_SITUATION: 'legal_situation_code', ACTIVITY: 'code_naf_elargi',
                              MIN_CA: 'chiffre_affaires_min', MAX_CA: 'chiffre_affaires_max', MIN_RES: 'resultat_min',
                              MAX_RES: 'resultat_max', MIN_EFF: 'tranche_effectif_min', MAX_EFF: 'tranche_effectif_max', REGION: 'region',
                              MIN_CAP: 'capital_min', MAX_CAP: 'capital_max',
                              MIN_AGE: 'age_dirigeant_min', MAX_AGE: 'age_dirigeant_max',
                              CREATION_DATE_START: 'date_creation_min', CREATION_DATE_END: 'date_creation_max',
                              COUNTRY: 'country_code', COMPANY_NUMBER: 'siren'}

    response_dictionary = {RESULTS: 'resultats', COMPANY_NUMBER: 'siren', TOTAL: 'total'}

    pappers_api_search_url = Config.PAPPERS_API_SEARCH_URL_FR
    pappers_api_company_url = Config.PAPPERS_API_COMPANY_URL_FR
    pappers_api_search_key = Config.PAPPERS_API_KEY_FR
    pappers_api_company_key = Config.PAPPERS_API_COMPANY_PERSO_KEY

    region_codes = []
    postal_codes = []
    legal_forms = []
    legal_situations = []
    activities = []

    def __init__(self):
        self.init_region_codes()
        self.init_postal_codes()
        self.init_legal_form()
        self.init_activities()

    def init_region_codes(self):
        with open(self.region_codes_file, mode='r', encoding='utf-8') as csv_file:
            lecteur_csv = csv.DictReader(csv_file, delimiter=';')
            for row in lecteur_csv:
                self.region_codes.append({"code": row['region_code'], "name": row['region_name']})
        self.region_codes = sorted(self.region_codes, key=lambda item: item['name'])

    def init_postal_codes(self):
        processed_postal_codes = []
        with open(self.postal_codes_file, mode='r', encoding='utf-8') as csv_file:
            lecteur_csv = csv.DictReader(csv_file, delimiter=';')
            for ligne in lecteur_csv:
                if ligne[CITY_COLUMN].strip() and not ligne[POSTAL_CODE_COLUMN] in processed_postal_codes:
                    self.postal_codes.append({"code_postal": ligne[POSTAL_CODE_COLUMN], "commune": ligne[CITY_COLUMN]})
                    processed_postal_codes.append(ligne[POSTAL_CODE_COLUMN])
        self.postal_codes = sorted(self.postal_codes, key=lambda item: int(item['code_postal']))

    def init_activities(self):
        df = pd.read_excel(self.activities_file)
        self.activities = [{'code': str(row['Code']), 'libelle': row['Libellé NAF, FINAL']} for _, row in df.iterrows() if str(row['Code']).endswith('Z')]
        print(self.activities)

    def init_legal_form(self):
        df = pd.read_excel(self.legal_form_file)
        self.legal_forms = [{'c': str(row['Code']), 'n': row['Libellé']} for _, row in df.iterrows()]
        print(self.legal_forms)