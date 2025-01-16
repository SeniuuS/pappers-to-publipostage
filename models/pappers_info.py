from config import Config

class PappersInfo:
    def __init__(self, data, country):
        nom_societe = data.get('name', '')
        head_office = data.get('head_office', {})

        address = ""

        if head_office:
            country_found = head_office.get('country', '')
            if country_found is None:
                country_found = Config.COUNTRIES[country]
            address = f"{head_office.get('address_line_1', '')} {head_office.get('postal_code', '')} {head_office.get('city', '')} {country_found}"

        nom_dirigeant = (
            f"{data.get('officers', [{}])[0].get('last_name', '')} {data.get('officers', [{}])[0].get('first_name', '')}"
            if data.get('officers') else ''
        )

        company_number = data.get('company_number', '')
        creation_date = data.get('date_of_creation', '')

        self.company_name = nom_societe
        self.creation_date = creation_date
        self.address = address
        self.owner_name = nom_dirigeant
        self.email = ''
        self.phone = ''
        self.company_number = company_number

    def add_officer_info(self, data):
        officers = data.get('officers', [])
        physical_officers = [physical_officer for physical_officer in officers if physical_officer['type'] == 'physical']
        nom_dirigeant = (
            f"{physical_officers[0].get('last_name', '')} {physical_officers[0].get('first_name', '')}"
            if physical_officers else ''
        )

        contacts = data.get('contacts', [])
        emails = [contact for contact in contacts if contact['type'] == 'email']
        email = emails[0]['value'] if emails else ''
        phones = [contact for contact in contacts if contact['type'] == 'phone']
        phone = phones[0]['value'] if phones else ''

        self.owner_name = nom_dirigeant
        self.email = email
        self.phone = phone