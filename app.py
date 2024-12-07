from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import requests
import config
from openpyxl import Workbook
from datetime import datetime

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

API_KEY = config.pappers_api_key
PAPPERS_API_URL = 'https://api.pappers.in/v1/company'

COUNTRIES = {'FR': 'France', 'BE': 'Belgium', 'CH': 'Switzerland'}

@app.route('/', methods=['GET', 'POST'])
def index():
    country = request.args.get('country', 'FR').upper()

    if request.method == 'POST':
        # Vérification du fichier uploadé
        if 'file' not in request.files or request.files['file'].filename == '':
            return render_template('index.html', error='Veuillez fournir un fichier texte valide.')

        country = request.form.get('country', 'FR').upper()
        file = request.files['file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Traiter le fichier
        result_filepath = process_file(filepath, country)
        return redirect(url_for('download', filename=os.path.basename(result_filepath)))

    return render_template('index.html', country=country)


def process_file(filepath, country):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Format : YYYYMMDD_HHMMSS
    result_filename = f'result_{timestamp}.xlsx'  # Nom du fichier avec timestamp
    result_filepath = os.path.join(app.config['RESULT_FOLDER'], result_filename)

    # Créer un workbook Excel
    wb = Workbook()
    ws = wb.active
    ws2 = wb.create_sheet("Summary")
    ws.title = "Liste Publi-postage"

    # Ajouter les en-têtes
    headers = [
        'Nom société', 'Adresse', 'Nom dirigeant',
        'Email', 'Téléphone', 'Numero d\'entreprise'
    ]
    headers2 = [
        'Numero d\'entreprise', 'Result'
    ]
    ws.append(headers)
    ws2.append(headers2)

    # Lire le fichier uploadé et appeler l'API
    with open(filepath, 'r') as infile:
        lines = infile.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            params = {'api_token': API_KEY ,'company_number': line, 'country_code': country, 'fields': 'officers,ubos,financials,documents,certificates,publications,establishments,contacts'}

            # Appel à l'API Pappers avec en-tête Authorization
            response = requests.get(
                PAPPERS_API_URL,
                params=params
            )

            # Gestion de la réponse
            if response.status_code == 200:
                data = response.json()
                nom_societe = data.get('name', '')
                head_office = data.get('head_office', {})
                country_found = head_office.get('country', '')
                if country_found is None:
                    country_found = COUNTRIES[country]
                adresse = f"{head_office.get('address_line_1', '')} {head_office.get('postal_code', '')} {head_office.get('city', '')} {country_found}"
                nom_dirigeant = (
                    f"{data.get('officers', [{}])[0].get('last_name', '')} {data.get('officers', [{}])[0].get('first_name', '')}"
                    if data.get('officers') else ''
                )
                email = data.get('emails', [])[0] if data.get('emails') else ''
                telephone = data.get('telephones', [])[0] if data.get('telephones') else ''
                company_number = data.get('company_number', '')

                # Ajouter la ligne au tableau
                ws.append([
                    nom_societe, adresse, nom_dirigeant,
                    email, telephone, company_number
                ])
                ws2.append([
                    line, "Information found"
                ])
            else:
                ws2.append([
                    line, f"{response.status_code} - {response.text}"
                ])

    # Sauvegarder le fichier Excel
    wb.save(result_filepath)
    return result_filepath


@app.route('/download/<filename>')
def download(filename):
    file_path = os.path.join(app.config['RESULT_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=False)