import json
import requests


def check_mandate_branch(mandate, phone):

    url = "https://libertyussd.com/api/get_mandate_branch/"

    payload = {'mandate': f'{mandate}',
               'phone': f'{phone}'}
    headers = {}

    response = requests.request("POST", url, headers=headers, data=payload)

    try:
        return json.loads(response.text)

    except:
        return response.text
