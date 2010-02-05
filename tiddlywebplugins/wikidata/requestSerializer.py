from tiddlyweb.serializations import SerializationInterface

from tiddlywebplugins.wikidata import templating


class Serialization(SerializationInterface):

    def tiddler_as(self, tiddler):
        template = templating.get_template(self.environ, 'request.html')
        return template.render(tiddler=tiddler,
                commonVars=templating.common_vars(self.environ))
