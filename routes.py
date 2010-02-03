import templating
import logging

from tiddlyweb.web.http import HTTP404
from tiddlywebplugins.utils import replace_handler, remove_handler
from emailAvox import emailAvox

def index(environ, start_response):
    template = templating.generate_template(["index.html","search.html"])
    
    start_response('200 OK', [
        ('Content-Type', 'text/html'),
        ('Pragma', 'no-cache')
        ])
    
    commonVars = templating.getCommonVars(environ)
    return template.render(commonVars=commonVars)

def template_route(environ, start_response):
    template_name = environ['wsgiorg.routing_args'][1]['template_file']
    
    if '../' in template_name:
        raise HTTP404('%s invalid' % template_name)
    
    if '.html' not in template_name:
       template_name = template_name + '.html'
       
    template = templating.generate_template([template_name])
        
    start_response('200 OK', [
        ('Content-Type', 'text/html'),
        ('Pragma', 'no-cache')
        ])
    
    commonVars = templating.getCommonVars(environ)
    return template.render(commonVars=commonVars)
    

def test_template_route(environ, start_response):
    template_name = 'test_'+environ['wsgiorg.routing_args'][1]['template_file']
    
    if '../' in template_name:
        raise HTTP404('%s invalid' % template_name)
    
    if '.html' not in template_name:
       template_name = template_name + '.html'
       
    template = templating.generate_test_template([template_name])
        
    start_response('200 OK', [
        ('Content-Type', 'text/html'),
        ('Pragma', 'no-cache')
        ])
    
    commonVars = templating.getCommonVars(environ)
    return template.render(commonVars=commonVars)

def get_fields_js(environ, start_response):
    from recordFields import getFields
    template = templating.generate_plain_template(['fields.js.html'])
    fields = getFields(environ)
    start_response('200 OK', [
        ('Content-Type', 'application/javascript'),
        ('Pragma', 'no-cache')
    ])
    return template.render(fields=fields)

def env(environ, start_response):

    from pprint import pformat

    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [pformat(environ)]
    
def verify(environ, start_response):
    from captcha import submit
    
    logging.debug(environ['tiddlyweb.query'])
    try:
        redirect = environ['tiddlyweb.query']['recaptcha_redirect'][0]
    except:
        redirect = environ['HTTP_REFERER'].split('?',1)[0]
    
    commonVars = templating.getCommonVars(environ)
    responseVars = {}
    notSpam = False
    if commonVars['usersign']['name'] == 'GUEST':
        challenge_field = environ['tiddlyweb.query']['recaptcha_challenge_field'][0]
        logging.debug('challenge_field: '+challenge_field)
        response_field = environ['tiddlyweb.query']['recaptcha_response_field'][0]
        logging.debug('response_field: '+response_field)
        private_key = "6Ld8HAgAAAAAAAyOgYXbOtqAD1yuTaOuwP8lpzX0"
        ip_addr = environ['REMOTE_ADDR']
        logging.debug('ip_addr: '+ip_addr)
    
        resp = submit(challenge_field, response_field, private_key, ip_addr)
        if resp.is_valid:
            responseVars['captcha'] = 1
            notSpam = True
        else:
            responseVars['captcha'] = 0
    else:
        notSpam = True
    
    if notSpam:
        try:
            emailAvox(environ['tiddlyweb.query'])
            valid = 1
        except KeyError as detail: # the hook for server-side validation
            responseVars['formError'] = detail.args[0]
            valid = 0
    
    if notSpam == False or valid == 0 or (responseVars.has_key('captcha') and responseVars['captcha'] == 0):
        responseVars['success'] = 0
    else:
        responseVars['success'] = 1
    
    redirect = redirect + '?success='+str(responseVars['success'])
    if responseVars.has_key('captcha'):
        redirect = redirect + '&captcha='+str(responseVars['captcha'])
    if responseVars.has_key('formError'):
        redirect = redirect +'&formError='+responseVars['formError']

    start_response('302 Found', [
            ('Content-Type', 'text/html'),
            ('Location', redirect),
            ('Pragma', 'no-cache')
            ])
    
    return ""

def init(config):
    config['selector'].add('/pages/{template_file:segment}', GET=template_route)
    config['selector'].add('/test/{template_file:segment}',GET=test_template_route)
    config['selector'].add('/index.html', GET=index)
    config['selector'].add('/verify', POST=verify)
    config['selector'].add('/lib/fields.js', GET=get_fields_js)
    config['selector'].add('/env', GET=env)
    replace_handler(config['selector'], '/', dict(GET=index))
    remove_handler(config['selector'], '/recipes')
    remove_handler(config['selector'], '/recipes/{recipe_name}')
    remove_handler(config['selector'], '/recipes/{recipe_name}/tiddlers')
    remove_handler(config['selector'], '/bags')
    remove_handler(config['selector'], '/bags/{bag_name}')
    remove_handler(config['selector'], '/bags/{bag_name}/tiddlers')
