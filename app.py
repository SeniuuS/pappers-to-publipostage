from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import requests
import config
from openpyxl import Workbook

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['RESULT_FOLDER'] = 'results'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(app.config['RESULT_FOLDER'], exist_ok=True)

API_KEY = config.pappers_api_key
PAPPERS_API_URL = 'https://api.pappers.fr/v2/entreprise'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Vérification du fichier uploadé
        if 'file' not in request.files or request.files['file'].filename == '':
            return render_template('index.html', error='Veuillez fournir un fichier texte valide.')

        file = request.files['file']
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)

        # Traiter le fichier
        result_filepath = process_file(filepath)
        return redirect(url_for('download', filename=os.path.basename(result_filepath)))

    return render_template('index.html')


def process_file(filepath):
    result_filepath = os.path.join(app.config['RESULT_FOLDER'], 'result.xlsx')

    # Créer un workbook Excel
    wb = Workbook()
    ws = wb.active
    ws2 = wb.create_sheet("Summary")
    ws.title = "Liste Publi-postage"

    # Ajouter les en-têtes
    headers = [
        'Nom société', 'Adresse', 'Nom dirigeant',
        'Email', 'Téléphone', 'SIREN', 'SIRET'
    ]
    headers2 = [
        'Siren/Siret', 'Result'
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

            # Vérifier si la ligne est un numéro SIREN ou SIRET valide
            if len(line) == 9 and line.isdigit():
                params = {'siren': line}
            elif len(line) == 14 and line.isdigit():
                params = {'siret': line}
            else:
                print(f"Ligne invalide : {line}")
                continue

            # Appel à l'API Pappers avec en-tête Authorization
            response = requests.get(
                PAPPERS_API_URL,
                headers={
                    'api-key': API_KEY
                },
                params=params
            )

            # Gestion de la réponse
            if response.status_code == 200:
                data = response.json()
                diffusable = data.get('diffusable')
                if diffusable:
                    # Extraire les données
                    nom_societe = data.get('nom_entreprise', '')
                    siege = data.get('siege', {})
                    adresse = f"{siege.get('adresse_ligne_1', '')} {siege.get('code_postal', '')} {siege.get('ville', '')} {siege.get('pays', '')}"
                    nom_dirigeant = (
                        data.get('representants', [{}])[0].get('nom_complet', '')
                        if data.get('representants') else ''
                    )
                    email = data.get('emails', [])[0] if data.get('emails') else ''
                    telephone = data.get('telephones', [])[0] if data.get('telephones') else ''
                    siren = data.get('siren', '')
                    siret = data.get('siege', {}).get('siret', '')

                    # Ajouter la ligne au tableau
                    ws.append([
                        nom_societe, adresse, nom_dirigeant,
                        email, telephone, siren, siret
                    ])
                    ws2.append([
                        line, "Information found"
                    ])
                else:
                    ws2.append([
                        line, "Not diffusable"
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