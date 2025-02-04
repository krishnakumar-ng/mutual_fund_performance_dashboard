import requests
import uuid, json


class MutualFundData:

    def get_historic_data_for_given_scheme(self, scheme_code:str):
        url = "https://api.mfapi.in/mf"

        if scheme_code == None or scheme_code == "":
            raise RuntimeError("scheme code is mandatory.")
        else:
            url = url + "/" + str(scheme_code)

        payload = {}
        headers = {
            'requestId': str(uuid.uuid4())
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        response = response.json()

        print("="*60)
        print(response)
        print("x"*60)

    @classmethod
    def get_all_mutual_funds_schemes(cls):
        url = "https://api.mfapi.in/mf"

        payload = {}
        headers = {
            'Accept': "application/json"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        response = response.json()

        return response

    def get_scheme_codes_for_given_mutual_funds(self, mutual_funds_list):
        response = MutualFundData.get_all_mutual_funds_schemes()

        mutual_funds_scheme_code_map = {}
        for mutual_fund in mutual_funds_list:
            for scheme in response:
                if scheme['schemeName'] == mutual_fund:
                    mutual_funds_scheme_code_map[mutual_fund] = scheme['schemeCode']

        return mutual_funds_scheme_code_map
