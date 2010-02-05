from tiddlyweb.serializations import SerializationInterface

from tiddlywebplugins.wikidata import templating


class Serialization(SerializationInterface):

    def tiddler_as(self, tiddler):
    #    query = self.environ['tiddlyweb.query']
    #    try:
    #        success = query['success'][0]
    #    except:
    #        success = None
    #    commonVars = templating.getCommonVars(self.environ)
    #    store = self.environ['tiddlyweb.store']
    #    userTiddler = Tiddler(commonVars['usersign']['name'])
    #    userTiddler.bag = self.environ['tiddlyweb.config']['userbag_bag']
    #    userTiddler = store.get(userTiddler)
    #    userFields = userTiddler.fields
    #    return template.render(tiddler=tiddler, commonVars=commonVars, success=success, userFields=userFields)
    
        template = templating.get_template(self.environ, 'challenge.html')
        return template.render(tiddler=tiddler,
                commonVars=templating.common_vars(self.environ))
