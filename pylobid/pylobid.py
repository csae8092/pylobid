import re
import requests
from jsonpath_ng import parse
from . utils import extract_coords


class GNDIdError(ValueError):
    """Exception raised if the GND-ID is invalid."""


class GNDNotFoundError(Exception):
    """Exception raised if the API returns Not Found for a GND-ID."""


class GNDAPIError(Exception):
    """Broad exception if something unexpected happens."""


class PyLobidClient():
    """Main Class to interact with LOBID-API."""

    def factory(self):
        """Return a matching instance for the GND URL or ID.

        - Type `PlaceOrGeographicName` returns a `PyLobidPlace` instance.
        - Type `CorporateBody` returns a `PyLobidOrg` instance.
        - Type `Person` returns a `PyLobidPerson` instance.
        - All other types a `PyLobidPerson` instance

        :return: An matching object for the GND URL or Id
        :rtype: `PyLobidPlace`, `PyLobidOrg`, `PyLobidPerson`, `PyLobidPerson`
        """
        if self.ent_dict == {}:
            raise ValueError(f'No data found for {self.gnd_url}')
        if not self.ent_type:
            raise ValueError(f'Unknown type for {self.gnd_url}')
        if self.is_person:
            output = PyLobidPerson(gnd_id=None, fetch_related=self.fetch_related)
            output.process_data(data=self.ent_dict)
        elif self.is_org:
            output = PyLobidOrg(gnd_id=None)
            output.process_data(data=self.ent_dict)
        elif self.is_place:
            output = PyLobidPlace(gnd_id=None)
            output.process_data(data=self.ent_dict)
        else:
            return self
        return output

    @property
    def gnd_id(self) -> str:
        """Return the GND ID, e.g. 118650130."""
        return self.__gnd_id

    @property
    def gnd_url(self) -> str:
        """Return the GND URL e.g. http://d-nb.info/gnd/118650130"""
        return f"{self.BASE_URL}/{self.gnd_id}" if self.gnd_id is not None else False

    @property
    def is_place(self) -> bool:
        """Return True if this instance is a place entity, False otherwise."""
        return 'PlaceOrGeographicName' in self.ent_type

    @property
    def is_org(self) -> bool:
        """Return True if this instance is an organization entity, False otherwise."""
        return 'CorporateBody' in self.ent_type

    @property
    def is_person(self) -> bool:
        """Return True if this instance is a person entity, False otherwise."""
        return 'Person' in self.ent_type

    @property
    def ent_type(self) -> list:
        """Return the entity type."""
        return self.ent_dict.get('type', [])

    @property
    def same_as(self) -> list:
        """Return a list of alternative norm-data-ids."""
        return self.get_same_as()

    @property
    def alt_names(self) -> list:
        """Return a list of alternative names."""
        return self.get_alt_names()

    @property
    def pref_name(self) -> str:
        """Return the preferred name."""
        return self.get_pref_name()

    def extract_id(self, url: str) -> str:
        """Extract the GND-ID from an GND-URL.

        :param url: A GND-URL, e.g. http://d-nb.info/gnd/118650130
        :type url: str

        :raises: GNDIdError if no GND-ID is found.
        :return: The GND-ID, e.g. 118650130
        :rtype: str
        """
        gnd_id = re.search(self.ID_PATTERN, url)
        if gnd_id is None:
            raise GNDIdError(f'Could not find GND-ID in "{url}"')
        return gnd_id.group()

    def get_entity_lobid_url(self, url: str) -> str:
        """creates a lobid-entity URL from an GND-URL

        :param url: A GND-URL, e.g. http://d-nb.info/gnd/118650130
        :type url: str

        :return: A LOBID-ENTITY-URL, e.g. http://lobid.org/gnd/116000562
        :rtype: str
        """
        self.__gnd_id = self.extract_id(url)
        return self.gnd_url

    def get_entity_json(self, url: str = None) -> dict:
        """Get the LOBID-JSON response of a given GND-URL.

        :param url: A GND_URL
        :type url: str, optional

        :raises: GNDNotFoundError, GNDAPIError
        :return: The matching JSON representation fetched from LOBID
        :rtype: dict
        """
        url = self.gnd_url if url is None else self.get_entity_lobid_url(url)
        response = requests.get(url, headers={'Accept': 'application/json'})
        if response.status_code == 404:
            raise GNDNotFoundError(f'Could not find a GND Entity for ID "{self.gnd_id}"')
        if not response.ok:
            raise GNDAPIError(f'GND API error code: {response.status_code}')
        return response.json()

    def get_same_as(self) -> list:
        """Get the list of alternative norm-data-ids.

        :return: A list of tuples like ('GeoNames', 'http://sws.geonames.org/2782067'),
        :rtype: list
        """
        return [(x['collection'].get('abbr', 'no_abbr'), x['id']) for x in self.ent_dict['sameAs']]

    def get_pref_name(self) -> str:
        """Get the preferred name.

        :return: The preferred Name vale, e.g. 'Assmann, Richard'
        :rtype: str
        """
        result = self.ent_dict.get('preferredName', '')
        return result

    def get_alt_names(self) -> list:
        """Get the list of alternative names.

        :return: a list of alternative names
        :rtype: list
        """
        ent_dict = self.ent_dict
        return next(iter([match.value for match in self.pref_alt_names_xpath.find(ent_dict)]), [])

    def __str__(self) -> str:
        return self.BASE_URL

    def __repr__(self) -> str:
        return f'<PyLobidClient {self.gnd_url}>'

    def __init__(self, gnd_id: str = None, fetch_related: bool = False) -> None:
        """Class constructor."""
        self.BASE_URL = "http://lobid.org/gnd"
        self.ID_PATTERN = r'([0-9]\w*-*[0-9]\w*)'
        self.coords_xpath = parse('$..hasGeometry')
        self.coords_regex = r'[+|-]\d+(?:\.\d*)?'
        self.pref_alt_names_xpath = parse('$.variantName')
        self.fetch_related = fetch_related
        self.__gnd_id = None
        self.ent_dict = {}
        self.process_data(gnd_id=gnd_id)

    def process_data(self, gnd_id: str = None, data: dict = None) -> None:
        """Fetch and/or process entity data.

        The arguments `gnd_id` and `data` are mutually exclusive.

        :param gnd_id: any kind of GND_URI/URL
        :type gnd_id: str, optional
        :param data: an already fetched ent_dict
        :type data: dict, optional
        """
        if data is not None and gnd_id is not None:
            raise ValueError('gnd_id and data mutually exclusive parameters')
        if data is not None and 'id' in data:
            _ = self.get_entity_lobid_url(data.get('id'))
            self.ent_dict = data
        elif gnd_id is not None:
            _ = self.get_entity_lobid_url(gnd_id)
            self.ent_dict = self.get_entity_json()


class PyLobidPlace(PyLobidClient):
    """A python class representing a Place Entity."""

    def get_coords_str(self) -> str:
        """Get a string of coordinates.

        :return: A string containing coordinates
        :rtype: str
        """
        coords_str = f"{[match.value for match in self.coords_xpath.find(self.ent_dict)]}"
        return coords_str

    def get_coords(self) -> list:
        """Get a list of coordinates.

        :return: A list of longitude, latitude coords like ['+009.689780', '+051.210970']
        :rtype: list
        """
        coords_str = self.get_coords_str()
        return extract_coords(coords_str)

    @property
    def coords(self) -> list:
        """Return a list of coordinates."""
        return self.get_coords()

    def __repr__(self) -> str:
        return f'<PyLobidPlace {self.gnd_url}>'


class PyLobidOrg(PyLobidClient):
    """A python class representing an Organisation Entity."""

    @property
    def located_in(self) -> list:
        """Return a list of locations."""
        return self.ent_dict.get('placeOfBusiness', [])

    def __repr__(self) -> str:
        return f'<PyLobidOrg {self.gnd_url}>'


class PyLobidPerson(PyLobidClient):
    """A python class representing a Person Entity."""

    def get_life_dates(self) -> dict:
        """Get birth- and death dates.

        :return: A dict with keys birth_date_str and death_date_str
        :rtype: dict
        """
        return {
            "birth_date_str": next(iter(self.ent_dict.get('dateOfBirth', [])), ''),
            "death_date_str": next(iter(self.ent_dict.get('dateOfDeath', [])), '')
        }

    def place_of_values(self, place_of: str = 'Birth') -> dict:
        """Find values for PlaceOfBirth/Death.

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
        """Get the LOBID-JSON of a PlaceOfBirth|Death (if present).

        :param place_of: Passed in value concatenates to 'PlaceOfBirth|Death' \
        defaults to 'Birth'
        :type place_of: str

        :return: The LOBID-JSON of the PlaceOfBirth|Death
        :rtype: dict
        """
        place_id = self.place_of_values(place_of).get('id')
        return {} if place_id is None else PyLobidPlace(place_id).ent_dict

    def get_coords_str(self, place_of: str = 'Birth') -> str:
        """Get a string of coordinates.

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
        """Get a list of coordinates.

        :param place_of: Passed in value concatenates to 'PlaceOfBirth|Death' \
        defaults to 'Birth'
        :type place_of: str

        :return: A list of longitude, latitude coords like ['+009.689780', '+051.210970']
        :rtype: list
        """
        coords_str = self.get_coords_str(place_of=place_of)
        return extract_coords(coords_str)

    def get_place_alt_name(self, place_of: str = 'Birth') -> list:
        """Get the list of alternative names.

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
        return self.gnd_url

    def __repr__(self) -> str:
        return f'<PyLobidPerson {self.gnd_url}>'

    def process_data(self, gnd_id: str = None, data: dict = None) -> None:
        """Fetch and/or process entity data.

        The arguments `gnd_id` and `data` are mutually exclusive.

        :param gnd_id: any kind of GND_URI/URL
        :type gnd_id: str, optional
        :param data: an already fetched ent_dict
        :type data: dict, optional
        """
        super().process_data(gnd_id=gnd_id, data=data)
        if self.ent_dict == {}:
            return
        if self.is_person:
            self.ent_dict.update(pylobid_born={}, pylobid_died={})
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
