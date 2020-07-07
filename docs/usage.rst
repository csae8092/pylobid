=====
Usage
=====

To use pylobid in a project::

    from pylobid.pylobid import PyLobidPerson

    # create a PyLobidPerson object from a gnd_id
    gnd_id = "http://d-nb.info/gnd/119315122"
    py_ent = PyLobidPerson(gnd_id, fetch_related=True)

    # birth- and death dates:
    py_ent.life_span
    # returns {'birth_date_str': '1873-12-23', 'death_date_str': '1933-03-15'}

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
