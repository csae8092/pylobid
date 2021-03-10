TEST_PERSON_DICTS = [
    {
        'id': "http://d-nb.info/gnd/119315122",
        'pylobid_born': {
            'id': 'https://d-nb.info/gnd/4066009-6',
            'name': 'Wien',
            'coords': ['+016.371690', '+048.208199']
        },
        'pylobid_died': {
            'id': 'https://d-nb.info/gnd/4066009-6',
            'name': 'Wien',
            'coords': ['+016.371690', '+048.208199']
        },
        'life_span': {
            'birth_date_str': '1873-12-23',
            'death_date_str': '1933-03-15'
        }
    },
    {
        'id': "http://d-nb.info/gnd/116586869",
        'pylobid_born': {
            'id': ''
        },
        'pylobid_died': {
            'id': ''
        },
        'life_span': {
            'birth_date_str': '1874',
            'death_date_str': ''
        }
    },
    {
        'id': "1069009253",
        'pylobid_born': {
            'id': 'https://d-nb.info/gnd/1028714-0'
        },
        'pylobid_died': {
            'id': 'https://d-nb.info/gnd/4317058-4'
        }
    },
    {
        'id': "136037585",
        'pylobid_born': {
            'id': ''
        },
        'pylobid_died': {
            'id': ''
        }
    }
]

TEST_INVALID_URLS = [
    "?!invalid_id",
    "example.com/",
    "https://dnb.de",
    "",
    "http://lobid.org/gnd"
]

TEST_UNKNOWN_IDS = [
    "01234-4321",
    "0123abc-0123def"
]

TEST_IDS_DICT = {
    "persons": [
        "http://d-nb.info/gnd/143073923",
        "http://d-nb.info/gnd/139696725",
        "138379769",
        "http://d-nb.info/gnd/118650130",
    ]
}

TEST_IDS_ARRAY = [
    "http://d-nb.info/gnd/118650130",
    "http://d-nb.info/gnd/4003366-1",
    "https://d-nb.info/gnd/16254097-8",
    "141768134",
    "http://lobid.org/gnd/12328631X",
    "http://lobid.org/gnd/4075434-0"
]

TEST_URL_PARSER_ARRAY = [
    ("http://d-nb.info/gnd/118650130", "118650130"),
    ("http://d-nb.info/gnd/4003366-1", "4003366-1"),
    ("https://d-nb.info/gnd/16254097-8", "16254097-8"),
    ("141768134", "141768134"),
    ("http://lobid.org/gnd/12328631X", "12328631X"),
    ("http://lobid.org/gnd/4075434-0", "4075434-0")
]

TEST_STRINGS_WKT = [
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

TEST_PERSON_IDS = [
    ("http://d-nb.info/gnd/119315122", True),
    ("http://d-nb.info/gnd/116586869", True),
    ("1069009253", True),
    ("136037585", True),
    ("http://lobid.org/gnd/4012995-0", False)
]

TEST_PLACE_IDS = [
    ("http://lobid.org/gnd/4012995-0", True),
    ("https://d-nb.info/gnd/4056905-6", True),
    ("https://d-nb.info/gnd/1069009253", False),
]


TEST_ORG_IDS = [
    ('http://d-nb.info/gnd/4443305-0', True),
    ('http://d-nb.info/gnd/5034132-7', True),
    ('http://d-nb.info/gnd/600902-5', True),
    ('http://d-nb.info/gnd/116616103X', True),
    ("http://lobid.org/gnd/4012995-0", False),
    ("https://d-nb.info/gnd/4056905-6", False),
    ('http://d-nb.info/gnd/4011750-9', True),
    ('http://d-nb.info/gnd/2168247-1', True),
    ('http://d-nb.info/gnd/82742-3', True),
    ('http://d-nb.info/gnd/11486-8', True),
    ('http://d-nb.info/gnd/80092-2', True),
    ('http://d-nb.info/gnd/1600912-5', True),
]

TEST_FACTORY = [(element[0], "is_org") for element in TEST_ORG_IDS if element[1]]
TEST_FACTORY += [(element[0], "is_place") for element in TEST_PLACE_IDS if element[1]]
TEST_FACTORY += [(element['id'], "is_person") for element in TEST_PERSON_DICTS]

TEST_ORG_NAMES_LOCATIONS = [
    {
        'id': 'http://d-nb.info/gnd/4443305-0',
        'pref_name': 'Accademia Roveretana degli Agiati',
        'located_in': [
            {
                'id': 'https://d-nb.info/gnd/4076860-0',
                'label': 'Rovereto'
            }
        ]
    },
    {
        'id': 'http://d-nb.info/gnd/5034132-7',
        'pref_name': 'K.K. Akademisches Staats-Gymnasium (Lemberg)',
        'located_in': [
            {
                'id': 'https://d-nb.info/gnd/4035304-7',
                'label': 'Lemberg'
            }
        ]
    },
    {
        'id': 'http://d-nb.info/gnd/600902-5',
        'pref_name': 'Akademisches Gymnasium (Wien)',
        'located_in': [
            {
                'id': 'https://d-nb.info/gnd/4066009-6',
                'label': 'Wien'
            }
        ]
    },
    {
        'id': 'http://d-nb.info/gnd/116616103X',
        'pref_name': 'Augsburger Allgemeine (-Alles was uns bewegt-)',
        'located_in': [
            {
                'id': 'https://d-nb.info/gnd/4003614-5',
                'label': 'Augsburg'
            }
        ]
    },
    {
        'id': 'http://d-nb.info/gnd/401873-4',
        'pref_name': 'Kaiserlich-Königliches Altstädter Akademisches Gymnasium (Prag)',
        'located_in': [
            {
                'id': 'https://d-nb.info/gnd/4076310-9',
                'label': 'Prag'
            }
        ]
    },
    {
        'id': 'http://d-nb.info/gnd/1224816-2',
        'pref_name': 'Stift Engelszell',
        'located_in': [
            {
                'id': 'https://d-nb.info/gnd/4342017-5',
                'label': 'Engelhartszell'
            },
            {
                'id': 'https://d-nb.info/gnd/4085581-8',
                'label': 'Engelhartszell-Engelszell'
            }
        ]
    },
    {
        'id': 'http://d-nb.info/gnd/4011750-9',
        'pref_name': 'Deutscher Bund (Körperschaft)',
        'located_in': []
    },
    {
        'id': 'http://d-nb.info/gnd/4534475-9',
        'pref_name': 'Diözese Großwardein (Katholische Kirche)',
        'located_in': []
    },
    {
        'id': 'http://d-nb.info/gnd/2168247-1',
        'pref_name': 'Carl Gerold’s Sohn Verlagsbuchhandlung',
        'located_in': [
            {
                'id': 'https://d-nb.info/gnd/4066009-6',
                'label': 'Wien'
            }
        ]
    },
    {
        'id': 'http://d-nb.info/gnd/82742-3',
        'pref_name': 'Landesschule (Schulpforte)',
        'located_in': [
            {
                'id': 'https://d-nb.info/gnd/1048249190',
                'label': 'Schulpforte'
            }
        ]
    },
]
