"""
Start at building test infrastructure for wiki-data.
"""

import os

from tiddlyweb.config import config
from tiddlyweb.store import Store
from tiddlyweb.model.tiddler import Tiddler
from tiddlywebplugins.wikidata import init
from tiddlywebplugins.mappingsql import sTiddler

def setup_module(module):
    init(config)
    environ = {'tiddlyweb.config': config}
    extra_store = config['server_store'][1]['extras'][0][1]
    environ['tiddlyweb.config']['server_store'] = extra_store
    module.store = Store(extra_store[0], extra_store[1], environ)
    module.session = module.store.storage.session
    # drop existing data
    module.session.query(sTiddler).delete()
    # fill in some test data
    populate()

def populate():
    os.system('mysql avox < dataextracts/miniwiki.dump')

def test_store():
    """
    make sure the data in the db, for testing, is okay.
    """
    assert 'wdsql' in '%s' % store.storage
    assert session.query(sTiddler).count() == 3000
    tiddler = Tiddler('2159077', 'avox')
    tiddler = store.get(tiddler)
    assert tiddler.fields['legal_name'] == 'Allianz Vie SA'
