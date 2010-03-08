import mangler
config = {
        'log_level': 'DEBUG',
        #'server_store': ['tiddlywebplugins.mappingsql', {'db_config': 'sqlite:///test.db'}],
        'secret': 'the bees are in the what',
        'system_plugins': [
            'tiddlywebplugins.wikidata',
            'tiddlywebplugins.methodhack',
            'tiddlywebplugins.pathinfohack',
            'tiddlywebplugins.static'],
        'maps_api_key': 'ABQIAAAAfIA5i-5lcivJMUvTzLDrmxQg7wZe1qASdla1M-DFyiqfOoWRghT6gGJohIOLIoy-3oR7sKWQfPvlxA', # http://wiki-data.com/
        }
