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
        'life_span': {'birth_date_str': '1873-12-23', 'death_date_str': '1933-03-15'}
    },
    {
        'id': "http://d-nb.info/gnd/116586869",
        'pylobid_born': {
            'id': ''
        },
        'pylobid_died': {
            'id': ''
        },
        'life_span': {'birth_date_str': '1874', 'death_date_str': ''}
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


TEST_PLACE_IDS = [
    ("http://lobid.org/gnd/4012995-0", True),
    ("https://d-nb.info/gnd/4056905-6", True),
    ("https://d-nb.info/gnd/1069009253", False),
]
