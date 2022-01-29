import requests

from config import get_env


class Characters:

    AUTH_KEY = get_env("API_KEY")
    BASE_URL = get_env("API_URL")

    def __init__(self):

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(self.AUTH_KEY),
        }

    def get_quote_by_id(self, id):
        url = self.BASE_URL + "/quote/{0}".format(id)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_character_by_id(self, id):
        url = self.BASE_URL + "/character/{0}".format(id)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_all_characters(self):
        url = self.BASE_URL + "/character"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_character_quote(self, id):
        url = self.BASE_URL + "/character/{0}/quote".format(id)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None


character_instance = Characters()