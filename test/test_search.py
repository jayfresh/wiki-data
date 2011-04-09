"""
Start at building test infrastructure for wiki-data.
"""

import os

from urlparse import parse_qs
from tiddlyweb.web.query import _update_tiddlyweb_query

from tiddlyweb.config import config
from tiddlyweb.store import Store
from tiddlyweb.model.tiddler import Tiddler
from tiddlywebplugins.wikidata import init
from tiddlywebplugins.mappingsql import sTiddler

def setup_module(module):
    init(config)
    module.environ = {'tiddlyweb.config': config}
    extra_store = config['server_store'][1]['extras'][0][1]
    environ['tiddlyweb.config']['server_store'] = extra_store
    module.store = Store(extra_store[0], extra_store[1], module.environ)
    module.session = module.store.storage.session
    # drop existing data
    module.session.query(sTiddler).delete()
    # fill in some test data
    populate()

def populate():
    os.system('mysql avox < dataextracts/miniwiki.dump')

def set_query_string(string):
    environ['tiddlyweb.query'] = {}
    query_data = parse_qs(string, keep_blank_values=True)
    _update_tiddlyweb_query(environ, query_data)

def test_store():
    """
    make sure the data in the db, for testing, is okay.
    """
    assert 'wdsql' in '%s' % store.storage
    assert session.query(sTiddler).count() == 3000
    tiddler = Tiddler('2159077', 'avox')
    tiddler = store.get(tiddler)
    assert tiddler.fields['legal_name'] == 'Allianz Vie SA'

def test_avid_search():
    """
    test we can get by avid
    """
    set_query_string('q=&avid=2159077')
    assert environ['tiddlyweb.query']['q'][0] == ''
    assert environ['tiddlyweb.query']['avid'][0] == '2159077'

    tiddlers = list(store.search(''))

    assert len(tiddlers) == 1
    tiddler = store.get(tiddlers[0])
    assert tiddler.title == '2159077'
    assert tiddler.fields['legal_name'] == 'Allianz Vie SA'

def test_query_with_fields():
    set_query_string('q=bank&avid=&adv_1_field=Operational+City&adv_1_value=London&adv_2_field=Operational+Country&adv_2_value=GBR')

    tiddlers = list(store.search(''))

    assert len(tiddlers) == 3

    assert [tiddler.title for tiddler in tiddlers] == ['2241075', '2408280', '4140665']
