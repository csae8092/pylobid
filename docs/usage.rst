=====
Usage
=====

Getting started
---------------

.. code-block:: python

    from pylobid.pylobid import PyLobidClient
    gnd_id = "http://d-nb.info/gnd/119315122"
    py_ent = PyLobidClient(gnd_id, fetch_related=True).factory()
    print(repr(py_ent))
    <PyLobidPerson http://lobid.org/gnd/119315122>

`PyLobidClient().factory()` returns the following instances based on the provided entity type:

- Type `PlaceOrGeographicName` returns a `PyLobidPlace` instance.
- Type `CorporateBody` returns a `PyLobidOrg` instance.
- Type `Person` returns a `PyLobidPerson` instance.
- All other types a `PyLobidPerson` instance

`PyLobidClient` and its derivatives can raise the following exceptions:

- `GNDIdError` If the GND-ID cannot be parsed from the provided URL or ID string.
- `GNDNotFoundError` If the GND cannot be found and the API endpoint responds with `404 Not Found`.
- `GNDAPIError` If the API endpoint response code is anything other than 200 or 404.

`GNDIdError` is a derivative of `ValueError`. All requests are done with the `requests` module and none of its exceptions are caught by this module.

Persons
-------

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
------

How to use PyLobidPlace object::

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


Organisations
-------------

How to use PyLobidOrg object::

    from pylobid.pylobid import PyLobidOrg

    pl_org = PyLobidOrg('4443305-0', fetch_related=False)
    for x in ['located_in', 'alt_names', 'same_as', 'pref_name']:
        print(f"{x}: {getattr(pl_org, x)}\n")

        located_in: [{'id': 'https://d-nb.info/gnd/4076860-0', 'label': 'Rovereto'}]

    alt_names: ['Imperial Regia Accademia scientifica e letteraria degli Agiati (Rovereto)', 'Accademia di scienze, lettere ed arti degli Agiati di Rovereto', 'Imperiale Regia Accademia Roveretana', 'Accademia degli Agiati (Rovereto)', 'Accademia Roveretana', 'I. R. Accademia Roveretana degli Agiati', 'I. R. Accademia di lettere e scienze degli Agiati (Rovereto)', 'Regia Accademia Roveretana degli Agiati', 'I. R. Accademia scientifica e letteraria degli Agiati (Rovereto)', 'Imperial Regia Accademia di lettere e scienze degli Agiati (Rovereto)', 'I. R. Accademia degli Agiati (Rovereto)', 'Imperiale Regia Accademia Scientifica e Letteraia degli Agiati', 'Imperiale Regia Accademia di Lettere e Scienze degli Agiati', 'Imperiale Regia Accademia di scienze, lettere ed arti degli Agiati (Rovereto)', 'Imperiale Regia Accademia di Scienze, Lettere ed Arti degli Agiati', 'Accademia degli Agiati (Rovereto, Accademia Roveretana degli Agiati)', 'Imperial Regia Accademia degli Agiati (Rovereto)', 'Imperial Regia Accademia Roveretana', 'Imperiale Regia Accademia di Scienze, Lettere ed Arti degli Agiati (Rovereto)', 'Accademia degli Agiati', 'Imperial Regia Accademia roveretana', 'Imperiale Regia Accademia Roveretana degli Agiati', 'Imperial Regia Accademia di scienze e lettere (Rovereto)', 'I. R. Accademia di scienze e lettere (Rovereto)']

    same_as: [('VIAF', 'http://viaf.org/viaf/310513758'), ('WIKIDATA', 'http://www.wikidata.org/entity/Q3603948'), ('DNB', 'https://d-nb.info/gnd/1085251314'), ('DNB', 'https://d-nb.info/gnd/4443305-0/about')]

    pref_name: Accademia Roveretana degli Agiati



WTForms validators
------------------

The `pylobid` module contains a validator for `WTForms <https://wtforms.readthedocs.io/en/3.0.x/>`_. With `pylobid.validators` you can validate the input from forms.

- Check if the provided GND URL or ID exists
- Check if the entity is a Person, Place or Organization.

.. code-block:: python

    import wtforms
    from pylobid import validators

    class GNDPersonForm(wtforms.Form):
        gnd_str = wtforms.StringField(
            label='GND ID or URL',
            validators=[validators.GNDPersonEntity()])

    form = GNDPersonFrom()
    # ... Do your form thing ...
    if form.validate():
        print('Form validation success')
    else:
        for error in form.errors:
            print(error)

Available validators:

- `validators.GNDPersonEntity()`
- `validators.GNDPlaceEntity()`
- `validators.GNDOrgEntity()`
- `validators.GNDValidator()`


