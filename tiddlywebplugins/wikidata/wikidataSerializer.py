import logging

from tiddlyweb.serializations.html import Serialization as HTML_Serializer

from tiddlywebplugins.wikidata import templating


class Serialization(HTML_Serializer):

    def __init__(self, environ=None):
        self.environ = environ
        try:
            self.maps_api_key = environ['tiddlyweb.config']['maps_api_key']
        except (TypeError, KeyError):
            self.maps_api_key = None

    def list_tiddlers(self, bag):
        logging.debug('in list_tiddlers')
        tiddlers = bag.list_tiddlers()
        template = templating.get_template(self.environ, 'collection.html')
        return template.render(tiddlers=tiddlers,
                commonVars=templating.common_vars(self.environ))

    def tiddler_as(self, tiddler):
        logging.debug('in tiddler_as')
        template = templating.get_template(self.environ, 'company.html')
        open_fields = self.environ['tiddlyweb.config']['mappingsql.open_fields']
        return template.render(tiddler=tiddler,
                maps_api_key=self.maps_api_key,
                commonVars=templating.common_vars(self.environ),
                open_fields=open_fields)
