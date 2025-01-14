import csv
import os

import pandas as pd

from helpers.json_helper import read_file_json

CITY_COLUMN = 'Municipality name (French)'
POSTAL_CODE_COLUMN = 'Postal Code'
REGION_CODE_COLUMN = 'Région code'

class Belgium:
    postal_codes_file = os.path.join('sources', 'postal-codes-belgium.csv')
    legal_form_file = os.path.join('sources', 'forme-juridique-belgium.json')
    legal_situation_file = os.path.join('sources', 'situation-juridique-belgium.json')
    activities_file = os.path.join('sources', 'TU_COM_NACEBEL_2008.xlsx')

    postal_codes = []
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

    def init_activities(self):
        df = pd.read_excel(self.activities_file)
        level_5_codes = df[df['LVL_NACEBEL'] == 5]
        self.activities = [{'code': str(row['CD_NACEBEL']), 'libelle': row['TX_NACEBEL_FR']} for _, row in level_5_codes.iterrows()]

    def init_legal_form(self):
        self.legal_forms = read_file_json(self.legal_form_file)

    def init_legal_situation(self):
        self.legal_situations = read_file_json(self.legal_situation_file)