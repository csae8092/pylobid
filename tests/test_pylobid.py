#!/usr/bin/env python
"""Tests for `pylobid` package."""

import unittest
from pylobid import utils
from pylobid import pylobid as pl
from .fixtures import *

BADEN_ALT_NAMES = [
    "Baden (Wienerwald)",
    "Baden bei Wien",
    "Stadtgemeinde Baden",
    "Stadtgemeinde Baden bei Wien"
]


class TestUtilsFunctions(unittest.TestCase):
    """Tests for utils package."""

    def test_000_extract_points(self):
        for item in TEST_STRINGS_WKT:
            points = utils.extract_coords(item[0])
            self.assertEqual(points[0], item[1][0], f"should be {item[0][0]}")
            self.assertEqual(points[1], item[1][1], f"should be {item[1][1]}")


class TestPylobidPlace(unittest.TestCase):
    """Tests for `pylobid` package."""

    def test_000_check_type(self):
        for item in TEST_PLACE_IDS:
            with self.subTest(place_id=item[0]):
                pl_place = pl.PyLobidPlace(item[0], fetch_related=False)
                self.assertEqual(pl_place.is_place, item[1], f"should be {item[1]}")

    def test_001_check_coords_type(self):
        for item in TEST_PLACE_IDS:
            with self.subTest(place_id=item[0]):
                pl_place = pl.PyLobidPlace(item[0], fetch_related=False)
                self.assertEqual(type(pl_place.coords), list, "should be a list")

    def test_002_check_coords(self):
        gnd_id = "https://d-nb.info/gnd/4066009-6"
        coords = ['+016.371690', '+048.208199']
        pl_place = pl.PyLobidPlace(gnd_id, fetch_related=False)
        self.assertEqual(pl_place.coords, coords, f"should be {coords}")

    def test_003_check_alt_names(self):
        gnd_id = "https://d-nb.info/gnd/4004168-2"
        pl_place = pl.PyLobidPlace(gnd_id, fetch_related=False)
        self.assertEqual(
            pl_place.alt_names, BADEN_ALT_NAMES, f"should be {BADEN_ALT_NAMES}"
        )

    def test_004_same_as(self):
        gnd_id = "https://d-nb.info/gnd/4004168-2"
        same_as = [
            # ('GeoNames', 'http://sws.geonames.org/2782067'),
            ('VIAF', 'http://viaf.org/viaf/234093638'),
            ('WIKIDATA', 'http://www.wikidata.org/entity/Q486450'),
            ('DNB', 'https://d-nb.info/gnd/2005587-0'),
            ('dewiki', 'https://de.wikipedia.org/wiki/Bahnhof_Baden_bei_Wien'),
        ]
        pl_place = pl.PyLobidPlace(gnd_id, fetch_related=False)
        for item in same_as:
            with self.subTest(same_as=item):
                self.assertTrue(item in pl_place.same_as)

    def test_005_pref_name(self):
        gnd_id = "https://d-nb.info/gnd/4004168-2"
        pref_name = 'Baden (Niederösterreich)'
        pl_place = pl.PyLobidPlace(gnd_id, fetch_related=False)
        self.assertEqual(pl_place.pref_name, pref_name, f"should be {pref_name}")

    def test_006_alt_name(self):
        gnd_id = "https://d-nb.info/gnd/4004168-2"
        pl_place = pl.PyLobidPlace(gnd_id, fetch_related=False)
        for item in BADEN_ALT_NAMES:
            with self.subTest(alt_name=item):
                self.assertTrue(item in pl_place.alt_names)


class TestPylobidClient(unittest.TestCase):
    """Tests for `pylobid` package."""

    def test_001_get_entity_lobid_url(self):
        pl_client = pl.PyLobidClient()
        for item in TEST_IDS_ARRAY:
            with self.subTest(gnd_str=item):
                lobid_url = pl_client.get_entity_lobid_url(item)
                self.assertEqual(lobid_url[0], 'h', "should be 'h'")

    def test_002_get_lobid_json(self):
        pl_client = pl.PyLobidClient()
        for item in TEST_IDS_ARRAY:
            with self.subTest(gnd_str=item):
                lobid_json = pl_client.get_entity_json(item)
                self.assertEqual(type(lobid_json), dict, f"{type(lobid_json)} should be a dict")

    def test_003_str(self):
        pl_client = pl.PyLobidClient()
        self.assertEqual(pl_client.__str__(), pl_client.BASE_URL, f"should be {pl_client.BASE_URL}")

    def test_005_url_parser(self):
        for input_str, id_str in TEST_URL_PARSER_ARRAY:
            with self.subTest(input_str=input_str, id_str=id_str):
                pl_client = pl.PyLobidClient(input_str)
                gnd_url = f"{pl_client.BASE_URL}/{id_str}"
                self.assertEqual(pl_client.gnd_url, gnd_url, f"gnd_url should be {gnd_url}")

    def test_006_factory(self):
        for gnd_id, entity_type in TEST_FACTORY:
            with self.subTest(gnd_id=gnd_id, entity_type=entity_type):
                entity_client = pl.PyLobidClient(gnd_id).factory()
                self.assertTrue(
                    getattr(entity_client, entity_type),
                    f"Entity should be {entity_type}"
                )

    def test_007_invalid_urls(self):
        for gnd_url in TEST_INVALID_URLS:
            with self.subTest(gnd_url=gnd_url):
                with self.assertRaises(pl.GNDIdError):
                    _ = pl.PyLobidClient(gnd_url)

    def test_008_unknown_ids(self):
        for gnd_id in TEST_UNKNOWN_IDS:
            with self.subTest(gnd_id=gnd_id):
                with self.assertRaises(pl.GNDNotFoundError):
                    _ = pl.PyLobidClient(gnd_id)


class TestPyLobidPerson(unittest.TestCase):
    """Tests for `pylobid` package."""

    def test_000_ent_type(self):
        for item in TEST_IDS_ARRAY:
            with self.subTest(gnd_id=item):
                pl_ent = pl.PyLobidPerson(item)
                self.assertEqual(
                    type(pl_ent.ent_type),
                    list,
                    f"type of {pl_ent.ent_type} should be a list"
                )

    def test_001_str(self):
        lobid_url = "http://lobid.org/gnd/4075434-0"
        pl_ent = pl.PyLobidPerson(lobid_url)
        self.assertEqual(pl_ent.__str__(), lobid_url, f"should be {lobid_url}")

    def test_002_is_person(self):
        for item in TEST_IDS_DICT['persons']:
            with self.subTest(gnd_id=item):
                pl_ent = pl.PyLobidPerson(item)
                self.assertTrue(pl_ent.is_person)

    def test_003_born_died_keys(self):
        for item in TEST_IDS_ARRAY:
            with self.subTest(gnd_id=item):
                pl_ent = pl.PyLobidPerson(item)
                if pl_ent.is_person:
                    ent_dict = pl_ent.ent_dict
                    self.assertTrue('pylobid_born' in ent_dict.keys())

    def test_004_born_died_keys(self):
        for item in TEST_PERSON_DICTS:
            with self.subTest(person=item):
                pl_ent = pl.PyLobidPerson(item['id'], fetch_related=True)
                self.assertEqual(
                    pl_ent.ent_dict['pylobid_born'].get('id', ''),
                    item['pylobid_born']['id'],
                    f"should be: {item['pylobid_born']['id']}"
                )
                self.assertEqual(
                    pl_ent.ent_dict['pylobid_died'].get('id', ''),
                    item['pylobid_died']['id'],
                    f"should be: {item['pylobid_died']['id']}"
                )

    def test_005_lifespans(self):
        for item in TEST_PERSON_DICTS:
            with self.subTest(person=item):
                pl_ent = pl.PyLobidPerson(item['id'])
                lifespan = pl_ent.get_life_dates()
                if 'life_span' in item.keys():
                    self.assertEqual( lifespan, item['life_span'], f"should be {item['life_span']}")
                else:
                    self.assertEqual(type(lifespan), dict, "should be a dict")

    def test_006_same_as(self):
        gnd_id = "1069009253"
        same_as = [
            ('VIAF', 'http://viaf.org/viaf/120106865'),
            ('DNB', 'https://d-nb.info/gnd/1069009253/about')
        ]
        pl_ent = pl.PyLobidPerson(gnd_id, fetch_related=False)
        self.assertEqual(pl_ent.same_as, same_as, f"should be {same_as}")

    def test_007_pref_name(self):
        gnd_id = "http://d-nb.info/gnd/1069009253"
        pref_name = 'Assmann, Richard'
        pl_item = pl.PyLobidPerson(gnd_id, fetch_related=False)
        self.assertEqual(pl_item.pref_name, pref_name, f"should be {pref_name}")


class TestPylobidOrg(unittest.TestCase):
    """Tests for `pylobid` package."""

    def test_001_pref_name(self):
        for item in TEST_ORG_NAMES_LOCATIONS:
            with self.subTest(org=item):
                pl_item = pl.PyLobidOrg(item['id'])
                self.assertEqual(
                    pl_item.pref_name,
                    item['pref_name'], f"{pl_item.pref_name} should be {item['pref_name']}"
                )

    def test_002_located_in(self):
        for item in TEST_ORG_NAMES_LOCATIONS:
            with self.subTest(org=item):
                pl_item = pl.PyLobidOrg(item['id'])
                self.assertEqual(
                    pl_item.located_in,
                    item['located_in'],
                    f"{pl_item.located_in} should be {item['located_in']}"
                )
