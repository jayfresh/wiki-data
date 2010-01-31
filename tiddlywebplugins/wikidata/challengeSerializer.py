import urllib
import logging

from tiddlyweb.serializations import SerializationInterface
from tiddlyweb.model.bag import Bag
from recordFields import getFields
from tiddlywebplugins.wikidata import templating

EXTENSION_TYPES = { 'challenge': 'text/x-challenge-html' }
SERIALIZERS = {
    'text/x-challenge-html': [
        'tiddlywebplugins.wikidata.challengeSerializer',
        'text/html; charset=UTF-8']
}

def init(config):
    config['extension_types'].update(EXTENSION_TYPES)
    config['serializers'].update(SERIALIZERS)


class Serialization(SerializationInterface):

    def tiddler_as(self, tiddler):
        bag = Bag('tmpbag', tmpbag=True)
        bag.add_tiddler(tiddler)
        template = templating.get_template(self.environ, 'challenge.html')
        try:
            query = self.environ['tiddlyweb.query']
            captcha = {}
            success = query['success'][0]
            if success == '1':
                captcha['success'] = True
            elif success == '0':
                captcha['failure'] = True
                try:
                   captcha['error'] = query['error'][0]
                except:
                   captcha['error'] = "Error not supplied"
        except:
            pass
        commonVars = templating.getCommonVars(self.environ)
        return template.render(tiddler=tiddler, commonVars=commonVars)
