from config import Config

class PappersInfoFR:
    def __init__(self, data, country):
        nom_societe = data.get('nom_entreprise', '')
        head_office = data.get('siege', {})

        address = ""

        if head_office:
            country_found = head_office.get('pays', '')
            if country_found is None:
                country_found = Config.COUNTRIES[country]
            address = f"{head_office.get('adresse_ligne_1', '')} {head_office.get('code_postal', '')} {head_office.get('ville', '')} {country_found}"

        self.company_name = nom_societe
        self.creation_date = data.get("date_creation", "")
        self.address = address
        self.activity = f"{data.get('code_naf', '')} - {data.get('domaine_activite', '')}"
        self.share_capital = ''
        self.legal_form = data.get('forme_juridique', '')
        self.active = 'En activité' if data.get('entreprise_cessee', 0) == 0 else 'Inactif'
        self.company_number = data.get('siren_formate', '')
        self.email = ''
        self.phone = ''
        self.owner_name = ''

        # Pas dispo en FR
        self.turnover = ''
        self.income = ''
        self.legal_situation = ''

    def add_officer_info(self, data):
        officers = data.get('representants', [])
        physical_officers = [physical_officer for physical_officer in officers if
                             physical_officer['personne_morale'] == False]
        nom_dirigeant = (
            physical_officers[0].get('nom_complet', '')
            if physical_officers else ''
        )

        self.share_capital = data.get('capital_formate', '')
        self.owner_name = nom_dirigeant
        self.email = data.get('email', '')
        self.phone = data.get('telephone', '')