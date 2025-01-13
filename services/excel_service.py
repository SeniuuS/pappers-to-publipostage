from datetime import datetime
import os
from openpyxl.workbook import Workbook
from config import Config

def create_excel_file(criterias, pappers_information):
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')  # Format : YYYYMMDD_HHMMSS
    result_filename = f'result_{timestamp}.xlsx'  # Nom du fichier avec timestamp
    result_filepath = os.path.join(Config.RESULT_FOLDER, result_filename)

    wb = Workbook()
    ws = wb.active
    ws2 = wb.create_sheet("Summary")
    ws.title = "Liste Publi-postage"

    headers = [
        'Nom société', 'Adresse', 'Nom dirigeant',
        'Email', 'Téléphone', 'Numero d\'entreprise'
    ]
    headers2 = [
        'Critère', 'Valeur'
    ]
    ws.append(headers)
    ws2.append(headers2)

    for pappers_information in pappers_information:
        pappers_info = pappers_information
        ws.append([
            pappers_info.company_name, pappers_info.address, pappers_info.owner_name,
            pappers_info.email, pappers_info.telephone, pappers_info.company_number
        ])

    for criteria in criterias:
        ws2.append([criteria['key'], criteria['value']])

    wb.save(result_filepath)
    return result_filepath