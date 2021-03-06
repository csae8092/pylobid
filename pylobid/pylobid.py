import re
import requests
from jsonpath_ng import parse
from . utils import extract_coords
from typing import Union

class PyLobidClient():
    """Main Class to interact with LOBID-API """

    def extract_id(self, url: str) -> Union[str, bool]:
        """extracts the GND-ID from an GND-URL

        :param url: A GND-URL, e.g. http://d-nb.info/gnd/118650130
        :type url: str, bool

        :return: The GND-ID, e.g. 118650130
        :rtype: str
        """
        return next(iter(re.findall(self.ID_PATTERN, url)), False)

    def get_entity_lobid_url(self, url: str) -> str:
        """creates a lobid-entity URL from an GND-URL

        :param url: A GND-URL, e.g. http://d-nb.info/gnd/118650130
        :type url: str

        :return: A LOBID-ENTITY-URL, e.g. http://lobid.org/gnd/116000562
        :rtype: str
        """
        gnd_id = self.extract_id(url)
        return f"{self.BASE_URL}/{gnd_id}" if gnd_id else False

    def get_entity_json(self, url: str) -> dict:
        """fetches the LOBID-JSON response of a given GND-URL

        :param url: A GND_URL
        :type url: str

        :return: The matching JSON representation fetched from LOBID
        :rtype: dict
        """
        request_url = self.get_entity_lobid_url(url)
        try:
            response = requests.request("GET", request_url, headers=self.HEADERS)
        except Exception as e:
            print(f"Request to LOBID-API for GND-URL {url} failed due to Error: {e}")
            return {}
        return response.json() if response.ok else {}

    def get_same_as(self) -> list:
        """ returns a list of alternative norm-data-ids

        :return: A list of tuples like ('GeoNames', 'http://sws.geonames.org/2782067'),
        :rtype: list
        """
        try:
            result = [(x['collection']['abbr'], x['id']) for x in self.ent_dict['sameAs']]
        except Exception as e:
            result = []
        return result

    def get_pref_name(self) -> str:
        """ returns the preferred name

        :return: The preferred Name vale, e.g. 'Assmann, Richard'
        :rtype: str
        """
        result = self.ent_dict.get('preferredName', '')
        return result

    def get_alt_names(self) -> list:
        """a list of alternative names

        :return: a list of alternative names
        :rtype: list

        """
        ent_dict = self.ent_dict
        return next(iter([match.value for match in self.pref_alt_names_xpath.find(ent_dict)]), [])

    def __str__(self) -> str:
        return self.BASE_URL

    def __init__(self) -> None:
        """Class constructor"""
        self.BASE_URL = "http://lobid.org/gnd"
        self.ID_PATTERN = "([0-9]\w*-*[0-9]\w*)"
        self.coords_xpath = parse('$..hasGeometry')
        self.coords_regex = r'[+|-]\d+(?:\.\d*)?'
        self.pref_alt_names_xpath = parse('$.variantName')
        self.HEADERS = {
            'Accept': 'application/json'
        }


class PyLobidPlace(PyLobidClient):
    """ A python class representing a Place Entity """

    def __init__(self, gnd_id: str, fetch_related: bool = False) -> None:
        """ initializes the class

        :param gnd_id: any kind of GND_URI/URL
        :type gnd_id: str
        :param fetch_related: should related objects be fetched
        :type fetch_related: bool

        :return: A PyLobidPlace instance
        """
        super().__init__()
        self.gnd_id = self.get_entity_lobid_url(gnd_id)
        self.ent_dict = self.get_entity_json(gnd_id)
        self.ent_type = self.ent_dict.get('type', False)
        self.is_place = 'PlaceOrGeographicName' in self.ent_type
        self.coords = self.get_coords()
        self.alt_names = self.get_alt_names()
        self.same_as = self.get_same_as()
        self.pref_name = self.get_pref_name()

    def get_coords_str(self) -> str:
        """get a string of coordinates

        :return: A string containing coordinates
        :rtype: str

        """
        coords_str = f"{[match.value for match in self.coords_xpath.find(self.ent_dict)]}"
        return coords_str

    def get_coords(self) -> list:
        """get a list of coordiantes

        :return: A list of longitute, latitude coords like ['+009.689780', '+051.210970']
        :rtype: list

        """
        coords_str = self.get_coords_str()
        return extract_coords(coords_str)


class PyLobidOrg(PyLobidClient):
    """ A python class representing an Organisation Entity """

    def __init__(self, gnd_id: str, fetch_related: bool = False) -> None:
        """ initializes the class

        :param gnd_id: any kind of GND_URI/URL
        :type gnd_id: str
        :param fetch_related: should related objects be fetched
        :type fetch_related: bool

        :return: A PyLobidOrg instance
        """
        super().__init__()
        self.gnd_id = self.get_entity_lobid_url(gnd_id)
        self.ent_dict = self.get_entity_json(gnd_id)
        self.ent_type = self.ent_dict.get('type', False)
        self.is_org = 'CorporateBody' in self.ent_type
        self.alt_names = self.get_alt_names()
        self.same_as = self.get_same_as()
        self.pref_name = self.get_pref_name()
        self.located_in = self.ent_dict.get('placeOfBusiness', [])


class PyLobidPerson(PyLobidClient):
    """ A python class representing a Person Entity """

    def get_life_dates(self) -> dict:
        """ returns birth- and death dates

        :return: A dict with keys birth_date_str and death_date_str
        :rtype: dict

        """
        return {
            "birth_date_str": next(iter(self.ent_dict.get('dateOfBirth', [])), ''),
            "death_date_str": next(iter(self.ent_dict.get('dateOfDeath', [])), '')
        }

    def place_of_values(self, place_of: str = 'Birth') -> dict:
        """find values for PlaceOfBirth/Death

        :param place_of: Passed in value concatenates to 'PlaceOfBirth|Death' \
        defaults to 'Birth'
        :type place_of: str

        :return: The ID of the Place
        :rtype: dict

        """
        value = f"placeOf{place_of}"
        result = self.ent_dict.get(value, False)
        return result[0] if isinstance(result, list) else {}

    def place_of_dict(self, place_of: str = 'Birth') -> dict:
        """get the LOBID-JSON of a PlaceOfBirth|Death (if present)

        :param place_of: Passed in value concatenates to 'PlaceOfBirth|Death' \
        defaults to 'Birth'
        :type place_of: str

        :return: The LOBID-JSON of the PlaceOfBirth|Death
        :rtype: dict

        """
        result = self.place_of_values(place_of)
        if result:
            place_id = result['id']
            return PyLobidPerson(place_id).ent_dict
        else:
            return {}

    def get_coords_str(self, place_of: str = 'Birth') -> str:
        """get a string of coordinates

        :param place_of: Passed in value concatenates to 'PlaceOfBirth|Death' \
        defaults to 'Birth'
        :type place_of: str

        :return: A string containing coordinates
        :rtype: str

        """
        place_of_key = "pylobid_born" if place_of == "Birth" else "pylobid_died"
        ent_dict = self.ent_dict.get(place_of_key, {})
        coords_str = f"{[match.value for match in self.coords_xpath.find(ent_dict)]}"
        return coords_str

    def get_coords(self, place_of: str = 'Birth') -> list:
        """get a list of coordinates

        :param place_of: Passed in value concatenates to 'PlaceOfBirth|Death' \
        defaults to 'Birth'
        :type place_of: str

        :return: A list of longitude, latitude coords like ['+009.689780', '+051.210970']
        :rtype: list

        """
        coords_str = self.get_coords_str(place_of=place_of)
        return extract_coords(coords_str)

    def get_place_alt_name(self, place_of: str = 'Birth') -> list:
        """a list of alternative names

        :param place_of: Passed in value concatenates to 'PlaceOfBirth|Death' \
        defaults to 'Birth'
        :type place_of: str

        :return: a list of alternative names
        :rtype: list

        """
        place_of_key = "pylobid_born" if place_of == "Birth" else "pylobid_died"
        ent_dict = self.ent_dict.get(place_of_key, {})
        return next(iter([match.value for match in self.pref_alt_names_xpath.find(ent_dict)]), [])

    def __str__(self) -> str:
        return self.gnd_id

    def __init__(self, gnd_id: str, fetch_related: bool = False) -> None:
        """ initializes the class

        :param gnd_id: any kind of GND_URI/URL
        :type gnd_id: str
        :param fetch_related: should related objects be fetched
        :type fetch_related: bool

        :return: A PyLobidPerson instance
        """
        super().__init__()
        self.gnd_id = self.get_entity_lobid_url(gnd_id)
        self.ent_dict = self.get_entity_json(gnd_id)
        self.ent_type = self.ent_dict.get('type', False)
        self.is_person = 'Person' in self.ent_type
        if self.is_person:
            self.ent_dict.update(pylobid_born={}, pylobid_died={})
        self.pref_name = self.get_pref_name()
        self.fetch_related = fetch_related
        self.pref_name_xpath = parse('$.preferredName')
        if self.fetch_related and self.is_person:
            self.ent_dict['pylobid_born'] = self.place_of_dict()
            if self.place_of_values().get('id', '') == self.place_of_values(place_of="Death").get('id', ''):
                self.ent_dict['pylobid_died'] = self.ent_dict['pylobid_born']
            else:
                self.ent_dict['pylobid_died'] = self.place_of_dict(place_of='Death')

        self.birth_place = {
            'person_id': self.gnd_id,
            'name': self.place_of_values().get('label', ''),
            'id': self.place_of_values().get('id', ''),
            'coords': self.get_coords(),
            'alt_names': self.get_place_alt_name()
        }
        self.death_place = {
            'person_id': self.gnd_id,
            'name': self.place_of_values(place_of='Death').get('label', ''),
            'id': self.place_of_values(place_of='Death').get('id', ''),
            'coords': self.get_coords(place_of='Death'),
            'alt_names': self.get_place_alt_name(place_of='Death')
        }
        self.life_span = self.get_life_dates()
        self.same_as = self.get_same_as()
