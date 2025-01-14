import json

def read_file_json(path):
    with open(path, mode='r', encoding='utf-8') as json_file:
        return json.load(json_file)