from tiddlywebplugins.templates import get_template as tw_get_template
from tiddlywebplugins.wikidata.recordFields import getFields

def get_template(environ, name):
    return tw_get_template(environ, name)
    
def getCommonVars(environ): # JRL: to make sure that templates have access to common fields
    fields = getFields(environ)
    usersign = environ['tiddlyweb.usersign']
    
    captcha = {}
    try:
        query = environ['tiddlyweb.query']
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

    return {
        'fields':fields,
        'usersign':usersign,
        'captcha':captcha
    }
