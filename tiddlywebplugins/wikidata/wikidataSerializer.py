import urllib
import logging

from tiddlyweb.serializations.html import Serialization as HTML_Serializer
from tiddlyweb.model.bag import Bag

from tiddlywebplugins.wikidata import templating
from tiddlywebplugins.wikidata.recordFields import getFields

EXTENSION_TYPES = { 'wd': 'text/html' }
SERIALIZERS = {
    'text/html': ['tiddlywebplugins.wikidata.wikidataSerializer',
        'text/html; charset=UTF-8'],
    'default': ['tiddlywebplugins.wikidata.wikidataSerializer',
        'text/html; charset=UTF-8']
}


def init(config):
    config['extension_types'].update(EXTENSION_TYPES)
    config['serializers'].update(SERIALIZERS)


class Serialization(HTML_Serializer):

    def __init__(self, environ=None):
        self.environ = environ
        try:
            self.maps_api_key = environ['tiddlyweb.config']['maps_api_key']
        except TypeError, KeyError:
            self.maps_api_key = None

    def list_tiddlers(self, bag):
        logging.debug('in list_tiddlers')
        tiddlers = bag.list_tiddlers()
        template = templating.get_template(self.environ, 'collection.html')
        commonVars = templating.getCommonVars(self.environ)
        return template.render(tiddlers=tiddlers, commonVars=commonVars)

    def tiddler_as(self, tiddler):
        logging.debug('in tiddler_as')
        bag = Bag('tmpbag', tmpbag=True)
        bag.add_tiddler(tiddler)
        template = templating.get_template(self.environ, 'company.html')
        commonVars = templating.getCommonVars(self.environ)
        open_fields = self.environ['tiddlyweb.config']['mappingsql.open_fields']
        return template.render(tiddler=tiddler, maps_api_key=self.maps_api_key, commonVars=commonVars, open_fields=open_fields)
