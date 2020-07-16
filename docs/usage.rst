=====
Usage
=====

Persons
--------

To use pylobid in a project::

    from pylobid.pylobid import PyLobidPerson

    # create a PyLobidPerson object from a gnd_id
    gnd_id = "http://d-nb.info/gnd/119315122"
    py_ent = PyLobidPerson(gnd_id, fetch_related=True)

    # preferred name
    print(pl_pers.pref_name)
    'Adams, John Quincy'

    # birth- and death dates:
    print(py_ent.life_span)
    returns {'birth_date_str': '1873-12-23', 'death_date_str': '1933-03-15'}

    # fetch data about the person's place of birth
    print(py_ent.birth_place)
    {'person_id': 'http://lobid.org/gnd/119315122', 'name': 'Wien', 'id': 'https://d-nb.info/gnd/4066009-6', 'coords': ['+016.371690', '+048.208199'], 'alt_names': ['Bundesunmittelbare Stadt Wien', 'Bécs', 'Bundesland Wien', 'Wīn', 'Vienna', 'Beč', 'Reichsgau Wien', 'Kaiserlich-Königliche Reichshaupt- und Residenzstadt Wien', 'Vjenë', 'Wienna', 'Vindobona (Wien)', 'Vin', 'Stadt Wien', 'Vienna Pannoniae', 'Wenia', 'Vídeň', 'Viedeň', 'Land Wien', 'Viennē', 'Reichshaupt- und Residenzstadt Wien', 'Wienn', 'Vienna Fluviorum', 'Vienne (Österreich)', 'K.K. Reichshaupt- und Residenzstadt Wien', 'Vinna', 'Bundeshauptstadt Wien', 'Vena', 'Vindobona', 'Wiedeń (Wien)', 'Vienna (Austriae)', 'Biennē', 'Gemeinde Wien', 'Dunaj', 'Vienne', 'Viena']}

    # fetch data about the person's place of death (which is again Vienna)
    print(py_ent.birth_death)
    {'person_id': 'http://lobid.org/gnd/119315122', 'name': 'Wien', 'id': 'https://d-nb.info/gnd/4066009-6', 'coords': ['+016.371690', '+048.208199'], 'alt_names': ['Bundesunmittelbare Stadt Wien', 'Bécs', 'Bundesland Wien', 'Wīn', 'Vienna', 'Beč', 'Reichsgau Wien', 'Kaiserlich-Königliche Reichshaupt- und Residenzstadt Wien', 'Vjenë', 'Wienna', 'Vindobona (Wien)', 'Vin', 'Stadt Wien', 'Vienna Pannoniae', 'Wenia', 'Vídeň', 'Viedeň', 'Land Wien', 'Viennē', 'Reichshaupt- und Residenzstadt Wien', 'Wienn', 'Vienna Fluviorum', 'Vienne (Österreich)', 'K.K. Reichshaupt- und Residenzstadt Wien', 'Vinna', 'Bundeshauptstadt Wien', 'Vena', 'Vindobona', 'Wiedeń (Wien)', 'Vienna (Austriae)', 'Biennē', 'Gemeinde Wien', 'Dunaj', 'Vienne', 'Viena']}

    # create a PyLobidPerson object without fetching related data
    py_ent = PyLobidPerson(gnd_id, fetch_related=False)
    print(py_ent.death_place)
    {'person_id': 'http://lobid.org/gnd/119315122', 'name': 'Wien', 'id': 'https://d-nb.info/gnd/4066009-6', 'coords': [], 'alt_names': []}

    # fetch same_as IDs
    pl_pers = PyLobidPerson('http://d-nb.info/gnd/1069009253', fetch_related=False)
    print(pl_pers.same_as)
    [('VIAF', 'http://viaf.org/viaf/120106865'), ('DNB', 'https://d-nb.info/gnd/1069009253/about')]


Places
--------

To use pylobid in a project::

    from pylobid.pylobid import PyLobidPlace

    pl_place = PyLobidPlace('4004168-2', fetch_related=False)
    print(pl_place.coords)
    ['+016.232500', '+048.005277']

    print(pl_place.pref_name)
    Baden (Niederösterreich)

    print(pl_place.alt_names)
    ['Baden, Wienerwald', 'Baden bei Wien', 'Stadtgemeinde Baden', 'Stadtgemeinde Baden bei Wien']

    print(pl_place.same_as)
    [('DNB', 'http://d-nb.info/gnd/4004168-2/about'), ('GeoNames', 'http://sws.geonames.org/2782067'), ('VIAF', 'http://viaf.org/viaf/234093638'), ('WIKIDATA', 'http://www.wikidata.org/entity/Q486450'), ('DNB', 'https://d-nb.info/gnd/2005587-0'), ('dewiki', 'https://de.wikipedia.org/wiki/Bahnhof_Baden_bei_Wien')]
