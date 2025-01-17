from config import Config

def can_do_detailed_export(checkbox, export_key):
    return checkbox == 'detailed' and export_key == Config.DETAILED_EXPORT_KEY