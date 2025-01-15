from datetime import datetime

DATE_FORMAT = '%Y-%m-%d'

def verify_date_range(start, end):
    start_date = datetime.strptime(start, DATE_FORMAT)
    end_date = datetime.strptime(end, DATE_FORMAT)
    if start_date > end_date:
        raise ValueError('Start date must be before end date')