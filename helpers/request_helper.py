import requests

def request_url(url):
    print(f"Requesting {url}")

    response = requests.get(url)

    if response.status_code == 200:
        print(f"Request {url} successful : 200")
        return response
    print(f"Error requesting {url} : {response.status_code}")
    return None