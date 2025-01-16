import logging

import requests

def request_url(url):
    logging.info(f"Requesting {url}")

    response = requests.get(url)

    if response.status_code == 200:
        logging.info(f"Request {url} successful : 200")
        return response
    logging.warning(f"Error requesting {url} : {response.status_code}")
    return None