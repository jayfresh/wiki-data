import mangler
config = {
        'log_level': 'DEBUG',
        'auth_systems': ['tiddlywebplugins.wikidata.loginform'],
        'server_store': ['tiddlywebplugins.diststore', { 
             'main': ['text', {'store_root': 'store'}], 
             'extras': [ 
                 (r'^avox$', ['tiddlywebplugins.mappingsql',
                     #{'db_config': 'mysql://avox@localhost/avox?charset=utf8'}]), 
                     {'db_config': 'sqlite:///test.db'}]), 
                     ], 
                 }],
        # 'server_store': ['mappingsql', {'db_config': 'mysql://avox@localhost/avox?charset=utf8'}],
        'secret': 'the bees are in the what',
        'system_plugins': [
            'tiddlywebplugins.wikidata',
            'tiddlywebplugins.methodhack',
            'tiddlywebplugins.pathinfohack',
            'tiddlywebplugins.static'],
        'maps_api_key': 'ABQIAAAAfIA5i-5lcivJMUvTzLDrmxQg7wZe1qASdla1M-DFyiqfOoWRghT6gGJohIOLIoy-3oR7sKWQfPvlxA', # http://wiki-data.com/
        }
