import csv
import json
import os

CITY_COLUMN = 'Municipality name (French)'
POSTAL_CODE_COLUMN = 'Postal Code'
REGION_CODE_COLUMN = 'Région code'

class Belgium:
    postal_codes_file = os.path.join('sources', 'postal-codes-belgium.csv')
    legal_form_file = os.path.join('sources', 'forme-juridique-belgium.json')
    legal_situation_file = os.path.join('sources', 'situation-juridique-belgium.json')
    postal_codes = []
    legal_forms = []
    legal_situations = []

    def __init__(self):
        self.init_postal_codes()
        self.init_legal_form()
        self.init_legal_situation()

    def init_postal_codes(self):
        with open(self.postal_codes_file, mode='r', encoding='utf-8') as csv_file:
            lecteur_csv = csv.DictReader(csv_file, delimiter=';')
            for ligne in lecteur_csv:
                if ligne[CITY_COLUMN].strip():
                    self.postal_codes.append({"code_postal": ligne[POSTAL_CODE_COLUMN], "commune": ligne[CITY_COLUMN]})

    def init_legal_form(self):
        with open(self.legal_form_file, mode='r', encoding='utf-8') as json_file:
            self.legal_forms = json.load(json_file)

    def init_legal_situation(self):
        with open(self.legal_situation_file, mode='r', encoding='utf-8') as json_file:
            self.legal_situations = json.load(json_file)