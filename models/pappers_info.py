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
        status = data.get('status', '')

        self.company_name = nom_societe
        self.creation_date = creation_date
        self.address = address
        self.owner_name = nom_dirigeant
        self.email = ''
        self.phone = ''
        self.activity = ''
        self.turnover = ''
        self.income = ''
        self.share_capital = f"{data.get('share_capital', '')} {data.get('share_capital_currency', '')}"
        self.legal_situation = ''
        self.legal_form = data.get('local_legal_form_name', '')
        self.active = 'En activité' if status == 'active' else 'Inactif'
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

        financials = data.get('financials', [])
        accounts = [account for account in financials if account['type'] == 'accounts']
        if accounts:
            self.turnover = f"{accounts[0].get('ratios').get('turnover')} {accounts[0].get('currency')}"
            self.income = f"{accounts[0].get('ratios').get('net_income')} {accounts[0].get('currency')}"

        activities = data.get('activities', [])
        for activity in activities:
            formatted_activity = f"{activity['code']}-{activity['name']}"
            if not formatted_activity in self.activity:
                self.activity = f"{self.activity}{formatted_activity},"
        if self.activity != '':
            self.activity = self.activity[:-1]

        self.legal_situation = data.get('legal_situation', '')

        self.owner_name = nom_dirigeant
        self.email = email
        self.phone = phone