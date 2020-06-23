#!/usr/bin/env python

"""Tests for `pylobid` package."""


import unittest

from pylobid import utils
from pylobid import pylobid as pl


class TestUtilsFunctions(unittest.TestCase):
    def test_000_extract_points(self):
        test_strings = [
            (
                "[[{'type': 'Point', 'asWKT': ['Point ( +023.599440 +038.463610 )']}]]",
                ['+023.599440', '+038.463610']
            ),
            (
                "[[{'type': 'Point', 'asWKT': ['Point (-023.599440 +038,\
                 +038.463610 +038.463610 )']}]]",
                ['-023.599440', '+038']
            )
        ]
        for x in test_strings:
            points = utils.extract_coords(x[0])
            self.assertEqual(points[0], x[1][0], f"should be {x[0][0]}")
            self.assertEqual(points[1], x[1][1], f"should be {x[1][1]}")


class TestPylobidClient(unittest.TestCase):
    """Tests for `pylobid` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_ID_PATTERN(self):
        pl_client = pl.PyLobidClient()
        GND_IDS = pl_client.TEST_IDS
        self.assertEqual(type(GND_IDS), list, "should be a list")

    def test_001_get_entity_lobid_url(self):
        pl_client = pl.PyLobidClient()
        for x in pl_client.TEST_IDS:
            lobid_url = pl_client.get_entity_lobid_url(x)
            self.assertEqual(lobid_url[0], 'h', "should be 'h'")

    def test_002_get_lobid_json(self):
        pl_client = pl.PyLobidClient()
        for x in pl_client.TEST_IDS:
            lobid_json = pl_client.get_entity_json(x)
            self.assertEqual(type(lobid_json), dict, f"{type(lobid_json)} should be a dict")

    def test_0003_str(self):
        pl_client = pl.PyLobidClient()
        self.assertEqual(
            pl_client.__str__(),
            pl_client.BASE_URL,
            f"should be {pl_client.BASE_URL}"
        )


class TestPylobidEntity(unittest.TestCase):
    """Tests for `pylobid` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_ent_type(self):
        ids = pl.PyLobidClient().TEST_IDS
        for x in ids:
            pl_ent = pl.PyLobidEntity(x)
            self.assertEqual(
                type(pl_ent.ent_type),
                list,
                f"type of {pl_ent.ent_type} should be a list"
            )

    def test_001_str(self):
        lobid_url = "http://lobid.org/gnd/4075434-0"
        pl_ent = pl.PyLobidEntity(lobid_url)
        self.assertEqual(
            pl_ent.__str__(),
            lobid_url,
            f"should be {lobid_url}"
        )
