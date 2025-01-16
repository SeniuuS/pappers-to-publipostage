import csv
import os

from config import Config
from helpers.consts import *

CITY_COLUMN = 'Libelle'
POSTAL_CODE_COLUMN = 'Code_Postal'
COMMUNE_CODE_COLUMN = 'Code_commune_INSEE'

class France:
    postal_codes_file = os.path.join('sources', 'postal-codes-france.csv')
    legal_form_file = os.path.join('sources', '')
    legal_situation_file = os.path.join('sources', '')
    activities_file = os.path.join('sources', '')

    criteria_dictionnary = {'status': 'Active', 'code_postal': 'Code Postal',
                            'categorie_juridique': 'Forme juridique',
                            'code_naf_elargi': 'Activités', 'chiffre_affaires_min': 'Chiffre d\'affaire minimum',
                            'chiffre_affaires_max': 'Chiffre d\'affaire maximum',
                            'resultat_min': 'Résultat minimum', 'resultat_max': 'Résultat maximum',
                            'tranche_effectif_min': 'Effectif minimum', 'tranche_effectif_max': 'Effectif maximum',
                            'date_creation_min': 'Date de création (min)',
                            'date_creation_max': 'Date de création (max)'}

    query_parameter_dictionary = {IN_ACTIVITY: 'status', POSTAL_CODE: 'code_postal', LEGAL_FORM: 'categorie_juridique',
                              LEGAL_SITUATION: 'legal_situation_code', ACTIVITY: 'code_naf_elargi',
                              MIN_CA: 'chiffre_affaires_min', MAX_CA: 'chiffre_affaires_max', MIN_RES: 'resultat_min',
                              MAX_RES: 'resultat_max', MIN_EFF: 'tranche_effectif_min', MAX_EFF: 'tranche_effectif_max',
                              CREATION_DATE_START: 'date_creation_min', CREATION_DATE_END: 'date_creation_max',
                              COUNTRY: 'country_code', COMPANY_NUMBER: 'siren'}

    response_dictionary = {RESULTS: 'resultats', COMPANY_NUMBER: 'siren', TOTAL: 'total'}

    pappers_api_search_url = Config.PAPPERS_API_SEARCH_URL_FR
    pappers_api_company_url = Config.PAPPERS_API_COMPANY_URL_FR
    pappers_api_search_key = Config.PAPPERS_API_KEY_FR
    pappers_api_company_key = Config.PAPPERS_API_COMPANY_PERSO_KEY

    postal_codes = []
    legal_forms = []
    legal_situations = []
    activities = []

    def __init__(self):
        self.init_postal_codes()
        # self.init_legal_form()
        # self.init_legal_situation()
        # self.init_activities()

    def init_postal_codes(self):
        processed_postal_codes = []
        with open(self.postal_codes_file, mode='r', encoding='utf-8') as csv_file:
            lecteur_csv = csv.DictReader(csv_file, delimiter=';')
            for ligne in lecteur_csv:
                if ligne[CITY_COLUMN].strip() and not ligne[POSTAL_CODE_COLUMN] in processed_postal_codes:
                    self.postal_codes.append({"code_postal": ligne[POSTAL_CODE_COLUMN], "commune": ligne[CITY_COLUMN]})
                    processed_postal_codes.append(ligne[POSTAL_CODE_COLUMN])
    #
    # def init_activities(self):
    #
    # def init_legal_form(self):
    #     self.legal_forms =
    #
    # def init_legal_situation(self):
    #     self.legal_situations =