import json
import re
import requests


class PyLobidClient():

    """ Main Class to interact with LOBID-API """

    def extract_id(self, url):
        """ extracts the GND-ID from an GND-URL
            :param url: A GND-URL, e.g. http://d-nb.info/gnd/118650130
            :returns: The GND-ID, e.g. 118650130
        """
        try:
            gnd_id = re.findall(self.ID_PATTERN, url)[0]
        except IndexError:
            gnd_id = False
        return gnd_id

    def get_entity_lobid_url(self, url):
        """ creates a lobid-entity URL from an GND-URL
            :param url: A GND-URL, e.g. http://d-nb.info/gnd/118650130
            :return: A LOBID-ENTITY-URL, e.g. http://lobid.org/gnd/116000562
        """
        gnd_id = self.extract_id(url)
        if gnd_id:
            lobid_url = f"{self.BASE_URL}/{gnd_id}"
        else:
            lobid_url = False
        return lobid_url

    def get_entity_json(self, url):
        """ fetches the LOBID-JSON response of a given GND-URL
            :param url: A GND_URL
            :return: The matching JSON representation fetched from LOBID
        """
        request_url = self.get_entity_lobid_url(url)
        try:
            response = requests.request("GET", request_url, headers=self.HEADERS)
        except Exception as e:
            print(f"Request to LOBID-API for GND-URL {url} failed due to Error: {e}")
            return False
        if response.ok:
            return response.json()
        else:
            False

    def __str__(self):
        return self.BASE_URL

    def __init__(self):
        """__init__
        """

        self.BASE_URL = "http://lobid.org/gnd"
        self.ID_PATTERN = "([0-9]+-*[0-9]*)$"
        self.TEST_IDS = [
            "http://d-nb.info/gnd/118650130",
            "http://d-nb.info/gnd/4003366-1",
            "https://d-nb.info/gnd/16254097-8",
            "141768134",
            "http://lobid.org/gnd/4075434-0"
        ]
        self.HEADERS = {
            'Accept': 'application/json'
        }


class PyLobidEntity(PyLobidClient):
    """ A python class representing a LOBID-OBJECT """

    def place_of_values(self, place_of='Birth'):
        value = f"placeOf{place_of}"
        result = self.ent_dict.get(value, False)
        if isinstance(result, list):
            return result[0]
        else:
            return False

    def place_of_dict(self, place_of='Birth'):
        result = self.place_of_values(place_of)
        if result:
            place_id = result['id']
            return PyLobidEntity(place_id).ent_dict
        else:
            False

    def __str__(self):
        return self.gnd_id

    def __init__(self, gnd_id=None):
        """ __init__
        """
        super().__init__()
        self.gnd_id = self.get_entity_lobid_url(gnd_id)
        self.ent_dict = self.get_entity_json(gnd_id)
        self.ent_type = self.ent_dict['type']
