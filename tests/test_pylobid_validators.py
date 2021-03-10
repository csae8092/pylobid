#!/usr/bin/env python
"""Tests for `pylobid_validators` package."""

import unittest
from .fixtures import *

try:
    import wtforms
except ModuleNotFoundError:
    wtforms = None
else:
    from pylobid import validators


class TestPylobidValidators(unittest.TestCase):
    """Tests for `pylobid_validators` package."""

    def setUp(self) -> None:
        if not wtforms:
            self.skipTest('wtforms not installed')

        class GNDPersonForm(wtforms.Form):
            gnd_str = wtforms.StringField('GND Id', [validators.GNDPersonEntity()])

        class GNDPlaceForm(wtforms.Form):
            gnd_str = wtforms.StringField('GND Id', [validators.GNDPlaceEntity()])

        class GNDOrgForm(wtforms.Form):
            gnd_str = wtforms.StringField('GND Id', [validators.GNDOrgEntity()])

        class GNDForm(wtforms.Form):
            gnd_str = wtforms.StringField('GND Id', [validators.GNDValidator()])

        self.GNDPersonForm = GNDPersonForm
        self.GNDPlaceForm = GNDPlaceForm
        self.GNDOrgForm = GNDOrgForm
        self.GNDForm = GNDForm

    def test_001_place_validator(self):
        for gnd_str, is_valid in TEST_PLACE_IDS:
            with self.subTest(gnd_str=gnd_str):
                form = self.GNDPlaceForm()
                form.gnd_str.data = gnd_str
                self.assertEqual(form.validate(), is_valid, form.errors)

    def test_002_org_validator(self):
        for gnd_str, is_valid in TEST_ORG_IDS:
            with self.subTest(gnd_str=gnd_str):
                form = self.GNDOrgForm()
                form.gnd_str.data = gnd_str
                self.assertEqual(form.validate(), is_valid, form.errors)

    def test_003_person_validator(self):
        for gnd_str, is_valid in TEST_PERSON_IDS:
            with self.subTest(gnd_str=gnd_str):
                form = self.GNDPersonForm()
                form.gnd_str.data = gnd_str
                self.assertEqual(form.validate(), is_valid, form.errors)

    def test_004_field_types(self):
        for field in [wtforms.StringField, wtforms.URLField]:
            with self.subTest(field=field):
                class Form(wtforms.Form):
                    gnd_str = field('GND Id', [validators.GNDPlaceEntity()])
                for gnd_str, is_valid in TEST_PLACE_IDS:
                    with self.subTest(gnd_str=gnd_str):
                        form = Form()
                        form.gnd_str.data = gnd_str
                        self.assertEqual(form.validate(), is_valid, form.errors)

    def test_005_invalid_urls(self):
        for gnd_str in TEST_INVALID_URLS:
            with self.subTest(gnd_str=gnd_str):
                form = self.GNDForm()
                form.gnd_str.data = gnd_str
                self.assertFalse(form.validate())

    def test_006_unknown_ids(self):
        for gnd_str in TEST_UNKNOWN_IDS:
            with self.subTest(gnd_str=gnd_str):
                form = self.GNDForm()
                form.gnd_str.data = gnd_str
                self.assertFalse(form.validate())
        for gnd_str, _ in TEST_FACTORY:
            with self.subTest(gnd_str=gnd_str):
                form = self.GNDForm()
                form.gnd_str.data = gnd_str
                self.assertTrue(form.validate())
