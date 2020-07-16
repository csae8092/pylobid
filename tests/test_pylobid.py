#!/usr/bin/env python

"""Tests for `pylobid` package."""


import unittest

from . fixtures import *

from pylobid import utils
from pylobid import pylobid as pl


class TestUtilsFunctions(unittest.TestCase):
    def test_000_extract_points(self):
        test_strings = TEST_STRINGS_WKT
        for x in test_strings:
            points = utils.extract_coords(x[0])
            self.assertEqual(points[0], x[1][0], f"should be {x[0][0]}")
            self.assertEqual(points[1], x[1][1], f"should be {x[1][1]}")


class TestPylobidPlace(unittest.TestCase):
    """Tests for `pylobid` package."""

    def setUp(self):
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_check_type(self):
        for x in TEST_PLACE_IDS:
            pl_place = pl.PyLobidPlace(x[0], fetch_related=False)
            self.assertEqual(pl_place.is_place, x[1], f"should be {x[1]}")

    def test_001_check_coords_type(self):
        for x in TEST_PLACE_IDS:
            pl_place = pl.PyLobidPlace(x[0], fetch_related=False)
            self.assertEqual(type(pl_place.coords), list, f"should be a list")

    def test_002_check_coords(self):
        id = "https://d-nb.info/gnd/4066009-6"
        coords = ['+016.371690', '+048.208199']
        pl_place = pl.PyLobidPlace(id, fetch_related=False)
        self.assertEqual(pl_place.coords, coords, f"should be {coords}")

    def test_003_check_alt_names(self):
        id = "https://d-nb.info/gnd/4004168-2"
        alt_names = [
            'Baden, Wienerwald',
            'Baden bei Wien',
            'Stadtgemeinde Baden',
            'Stadtgemeinde Baden bei Wien'
        ]
        pl_place = pl.PyLobidPlace(id, fetch_related=False)
        self.assertEqual(pl_place.alt_names, alt_names, f"should be {alt_names}")

    def test_004_same_as(self):
        id = "https://d-nb.info/gnd/4004168-2"
        same_as = [
            ('DNB', 'http://d-nb.info/gnd/4004168-2/about'),
            ('GeoNames', 'http://sws.geonames.org/2782067'),
            ('VIAF', 'http://viaf.org/viaf/234093638'),
            ('WIKIDATA', 'http://www.wikidata.org/entity/Q486450'),
            ('DNB', 'https://d-nb.info/gnd/2005587-0'),
            ('dewiki', 'https://de.wikipedia.org/wiki/Bahnhof_Baden_bei_Wien')
        ]
        pl_place = pl.PyLobidPlace(id, fetch_related=False)
        self.assertEqual(pl_place.same_as, same_as, f"should be {same_as}")


class TestPylobidClient(unittest.TestCase):
    """Tests for `pylobid` package."""

    def setUp(self):
        pass

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_001_get_entity_lobid_url(self):
        pl_client = pl.PyLobidClient()
        for x in TEST_IDS_ARRAY:
            lobid_url = pl_client.get_entity_lobid_url(x)
            self.assertEqual(lobid_url[0], 'h', "should be 'h'")

    def test_002_get_lobid_json(self):
        pl_client = pl.PyLobidClient()
        for x in TEST_IDS_ARRAY:
            lobid_json = pl_client.get_entity_json(x)
            self.assertEqual(type(lobid_json), dict, f"{type(lobid_json)} should be a dict")

    def test_003_str(self):
        pl_client = pl.PyLobidClient()
        self.assertEqual(
            pl_client.__str__(),
            pl_client.BASE_URL,
            f"should be {pl_client.BASE_URL}"
        )


class TestPyLobidPerson(unittest.TestCase):
    """Tests for `pylobid` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_ent_type(self):
        ids = TEST_IDS_ARRAY
        for x in ids:
            pl_ent = pl.PyLobidPerson(x)
            self.assertEqual(
                type(pl_ent.ent_type),
                list,
                f"type of {pl_ent.ent_type} should be a list"
            )

    def test_001_str(self):
        lobid_url = "http://lobid.org/gnd/4075434-0"
        pl_ent = pl.PyLobidPerson(lobid_url)
        self.assertEqual(
            pl_ent.__str__(),
            lobid_url,
            f"should be {lobid_url}"
        )

    def test_002_is_person(self):
        ids = TEST_IDS_DICT['persons']
        for x in ids:
            pl_ent = pl.PyLobidPerson(x)
            self.assertTrue(
                pl_ent.is_person
            )

    def test_003_born_died_keys(self):
        ids = TEST_IDS_ARRAY
        for x in ids:
            pl_ent = pl.PyLobidPerson(x)
            if pl_ent.is_person:
                ent_dict = pl_ent.ent_dict
                self.assertTrue('pylobid_born' in ent_dict.keys())

    def test_004_born_died_keys(self):
        for x in TEST_PERSON_DICTS:
            pl_ent = pl.PyLobidPerson(
                x['id'],
                fetch_related=True
            )
            self.assertEqual(
                pl_ent.ent_dict['pylobid_born'].get('id', ''),
                x['pylobid_born']['id'],
                f"should be: {x['pylobid_born']['id']}"
            )
            self.assertEqual(
                pl_ent.ent_dict['pylobid_died'].get('id', ''),
                x['pylobid_died']['id'],
                f"should be: {x['pylobid_died']['id']}"
            )

    def test_005_lifespans(self):
        for x in TEST_PERSON_DICTS:
            pl_ent = pl.PyLobidPerson(
                x['id']
            )
            lifespan = pl_ent.get_life_dates()
            if 'life_span' in x.keys():
                self.assertEqual(
                    lifespan, x['life_span'],
                    f"should be {x['life_span']}"
                )
            else:
                self.assertEqual(
                    type(lifespan), dict, "should be a dict"
                )

    def test_006_same_as(self):
        id = "1069009253"
        same_as = [
            ('VIAF', 'http://viaf.org/viaf/120106865'),
            ('DNB', 'https://d-nb.info/gnd/1069009253/about')
        ]
        pl_ent = pl.PyLobidPerson(id, fetch_related=False)
        self.assertEqual(pl_ent.same_as, same_as, f"should be {same_as}")
