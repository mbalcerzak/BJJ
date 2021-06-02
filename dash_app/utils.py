import json


def get_load_json_data_all():
    with open(f'Data/bjj_overall.json', 'r') as f:
        file = json.load(f)

    return file


def get_list(name: str) -> dict:
    with open(f'Dictionaries/{name}.json', 'r') as f:
        file = json.load(f)

    sorted_list = sorted(file[name])

    options = []
    for key in sorted_list:
        options.append({'label': key, 'value': key})

    return options


def get_genders():
    return [
        {'label': 'Male', 'value': 'Male'},
        {'label': 'Female', 'value': 'Female'}
    ]