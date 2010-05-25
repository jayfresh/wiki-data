"""
Static configuration data for wiki-data.
This can be overridden in tiddlywebconfig.py
"""

config = {
        'auth_systems': ['tiddlywebplugins.wikidata.loginform'],
        'system_plugins': ['tiddlywebplugins.jsonp'],
        'server_store': ['tiddlywebplugins.diststore', {
            'main': ['text', {'store_root': 'store'}],
            'extras': [
                (r'^avox$', ['tiddlywebplugins.wikidata.wdsql',
                    {'db_config': 'mysql://avox@localhost/avox?charset=utf8'}]),
                    #{'db_config': 'sqlite:///test.db'}]),
                ],
            }],
        'mappingsql.table': 'avox',
        'mappingsql.bag': 'avox',
        'mappingsql.id_column': 'avid',
        'mappingsql.open_fields': [
             'avid',
             'legal_name',
             'previous_name_s_',
             'trades_as_name_s_',
             'trading_status',
             'company_website',
             'registered_country',
             'operational_po_box',
             'operational_floor',
             'operational_building',
             'operational_street_1',
             'operational_street_2',
             'operational_street_3',
             'operational_city',
             'operational_state',
             'operational_country',
             'operational_postcode',
             'entity_type'
        ],
        'mappingsql.default_search_fields': [
             'legal_name',
             'previous_name_s_',
             'trades_as_name_s_',
        ],
        'mappingsql.full_text': True,
        'mappingsql.limit': 50,
        'extension_types': {
            'challenge': 'text/x-challenge-html',
            'request': 'text/x-request-html',
            'wd': 'text/html'
            },
        'serializers': {
            'text/x-challenge-html': [
                'tiddlywebplugins.wikidata.challengeSerializer',
                'text/html; charset=UTF-8'],
            'text/x-request-html': [
                'tiddlywebplugins.wikidata.requestSerializer',
                'text/html; charset=UTF-8'],
            'text/html': [
                'tiddlywebplugins.wikidata.wikidataSerializer',
                'text/html; charset=UTF-8'],
            'default': [
                'tiddlywebplugins.wikidata.wikidataSerializer',
                'text/html; charset=UTF-8']
            },
        }
