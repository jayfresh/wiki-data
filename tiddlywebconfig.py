config = {
        'system_plugins': ['tiddlywebplugins.wikidata'],
        'log_level': 'DEBUG',
        'twanager_plugins': ['tiddlywebplugins.wikidata'],
        'server_store': ['tiddlywebplugins.diststore', {
            'main': ['text', {'store_root': 'store'}],
            'extras': [
                (r'^avox$', ['tiddlywebplugins.wikidata.wdsql',
                    {'db_config': 'mysql://avox@localhost/avoxtest?charset=utf8'}]),
                    #{'db_config': 'sqlite:///test.db'}]),
                ],
            }],
        }
