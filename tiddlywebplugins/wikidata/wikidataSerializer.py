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
        resultcount = self.environ.get('tiddlyweb.mappingsql.count', 0)
        # might not need this bit
        try:
            index = self.environ['tiddlyweb.query']['index'][0]
        except KeyError:
            index = 0
        progress = {}
        if index == 0:
            progress['start'] = True
        elif index == resultcount:
            progress['end'] = True
        else:
            progress['middle'] = True
        ### to here
        template = templating.get_template(self.environ, 'collection.html')
        return template.render(tiddlers=tiddlers, resultcount=resultcount,
                commonVars=templating.common_vars(self.environ), progress=progress, query=self.environ['tiddlyweb.query'], pageDistance=self.environ['tiddlyweb.config']['mappingsql.limit'])

    def tiddler_as(self, tiddler):
        logging.debug('in tiddler_as')
        template = templating.get_template(self.environ, 'company.html')
        open_fields = self.environ['tiddlyweb.config']['mappingsql.open_fields']
        return template.render(tiddler=tiddler,
                maps_api_key=self.maps_api_key,
                commonVars=templating.common_vars(self.environ),
                open_fields=open_fields)
