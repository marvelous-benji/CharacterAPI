'''
This module contains utility class
for interacting with the third-party API
'''


import requests

from config import get_env


class Characters:

    AUTH_KEY = get_env("API_KEY")
    BASE_URL = get_env("API_URL")

    def __init__(self):
        '''
        Class initializer. I have chosen to use the
        string.format method rather than f-strings since 
        it's compatible with version of Python lower than 3.7
        unlike the f-strings form.
        '''

        self.headers = {
            "Content-Type": "application/json",
            "Authorization": "Bearer {0}".format(self.AUTH_KEY),
        }

    def get_quote_by_id(self, id):
        '''
        Returns quote for a particular quote id
        '''

        url = self.BASE_URL + "/quote/{0}".format(id)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_character_by_id(self, id):
        '''
        Returns character information for a particular character id
        '''

        url = self.BASE_URL + "/character/{0}".format(id)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_all_characters(self):
        '''
        Returns information regarding all characters
        '''

        url = self.BASE_URL + "/character"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None

    def get_character_quote(self, id):
        '''
        Returns quote for a particular character given its id
        '''

        url = self.BASE_URL + "/character/{0}/quote".format(id)
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            return response.json()
        return None


character_instance = Characters() # creates a singleton instance