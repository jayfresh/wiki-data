from tiddlywebplugins.templates import get_template as tw_get_template
from tiddlywebplugins.wikidata.recordFields import getFields, getTooltips
from tiddlywebplugins.wikidata.captcha import process_captcha

def get_template(environ, name):
    return tw_get_template(environ, name)
    
def common_vars(environ):
    """
    To make sure that templates have access to common fields.
    """
    fields = getFields(environ)
    tooltips = getTooltips()
    usersign = environ['tiddlyweb.usersign']
    if not 'fields' in usersign:
        usersign['fields'] = {'name': ''}
    captcha = process_captcha(environ)
    query = environ['tiddlyweb.query']

    return {'fields':fields, 'tooltips':tooltips, 'usersign':usersign, 'captcha':captcha, 'query':query}
