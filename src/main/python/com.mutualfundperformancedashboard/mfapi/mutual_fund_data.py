import requests
import pandas as pd


class MutualFundData:

    def get_scheme_details(self, scheme_code: int):
        """
        Fetches scheme details from the API.

        Args:
        scheme_code: Scheme code for the mutual fund.

        Returns:
        A dictionary containing scheme details (scheme name, etc.).
        """

        url = f"https://api.mfapi.in/mf/{scheme_code}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        return response.json()['meta']

    def get_nav_history(self, scheme_code: int):
        """
        Fetches historical NAV data for the scheme.

        Args:
            scheme_code: Scheme code for the mutual fund.

        Returns:
            A pandas DataFrame containing the NAV history.
        """

        url = f"https://api.mfapi.in/mf/{scheme_code}"
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for bad status codes
        df = pd.DataFrame(response.json()['data'])
        df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
        df.set_index('date', inplace=True)
        return df

    def get_all_mutual_funds_schemes(self):
        url = "https://api.mfapi.in/mf"

        payload = {}
        headers = {
            'Accept': "application/json"
        }

        response = requests.request("GET", url, headers=headers, data=payload)

        response = response.json()

        return response

    def get_scheme_codes_for_given_mutual_funds(self, mutual_funds_list):
        response = self.get_all_mutual_funds_schemes()

        mutual_funds_scheme_code_map = {}
        for mutual_fund in mutual_funds_list:
            for scheme in response:
                if scheme['schemeName'] == mutual_fund:
                    mutual_funds_scheme_code_map[mutual_fund] = scheme['schemeCode']

        return mutual_funds_scheme_code_map
