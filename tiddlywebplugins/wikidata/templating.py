from tiddlywebplugins.templates import get_template as tw_get_template
from tiddlywebplugins.wikidata.recordFields import getFields
from tiddlywebplugins.wikidata.captcha import process_captcha

def get_template(environ, name):
    return tw_get_template(environ, name)
    
def common_vars(environ):
    """
    To make sure that templates have access to common fields.
    """
    fields = getFields(environ)
    usersign = environ['tiddlyweb.usersign']
    captcha = process_captcha(environ)

    return {'fields':fields, 'usersign':usersign, 'captcha':captcha}
