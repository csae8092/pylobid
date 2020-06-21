#!/usr/bin/env python

"""Tests for `pylobid` package."""


import unittest

from pylobid import pylobid as pl


class TestPylobid(unittest.TestCase):
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
