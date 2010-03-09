import time
import logging
import socket

import tiddlywebplugins.logout
import tiddlywebplugins.magicuser
import tiddlywebplugins.jsonp

from tiddlywebplugins.wikidata import templating
from tiddlywebplugins.wikidata.emailAvox import emailAvox
from tiddlywebplugins.wikidata.sendEmail import send as send_email
from tiddlywebplugins.wikidata.recordFields import getFields
from tiddlywebplugins.wikidata import captcha
from tiddlywebplugins.wikidata.config import config as local_config

from tiddlyweb.util import merge_config
from tiddlyweb.store import NoUserError
from tiddlyweb.model.user import User
from tiddlyweb.model.tiddler import Tiddler
from tiddlyweb.web.http import HTTP404, HTTP302, HTTP303
from tiddlyweb.web.util import server_base_url
from tiddlywebplugins.utils import (replace_handler, remove_handler,
        require_role, ensure_bag)


def index(environ, start_response):
    template = templating.get_template(environ, 'index.html')
    
    start_response('200 OK', [
        ('Content-Type', 'text/html'),
        ('Pragma', 'no-cache')
        ])
    
    return template.render(commonVars=templating.common_vars(environ))


def template_route(environ, start_response):
    template_name = environ['wsgiorg.routing_args'][1]['template_file']
    
    if '../' in template_name:
        raise HTTP404('%s invalid' % template_name)
    
    if '.html' not in template_name:
        template_name = template_name + '.html'
       
    template = templating.get_template(environ, template_name)
        
    start_response('200 OK', [
        ('Content-Type', 'text/html'),
        ('Pragma', 'no-cache')
        ])
    
    return template.render(commonVars=templating.common_vars(environ))
    

def test_template_route(environ, start_response):
    template_name = 'test_'+environ['wsgiorg.routing_args'][1]['template_file']
    
    if '../' in template_name:
        raise HTTP404('%s invalid' % template_name)
    
    if '.html' not in template_name:
        template_name = template_name + '.html'
       
    template = templating.get_template(environ, template_name)
        
    start_response('200 OK', [
        ('Content-Type', 'text/html'),
        ('Pragma', 'no-cache')
        ])
    
    return template.render(commonVars=templating.common_vars(environ))


def get_fields_js(environ, start_response):
    template = templating.get_template(environ, 'fields.js.html')
    fields = getFields(environ)
    start_response('200 OK', [
        ('Content-Type', 'application/javascript'),
        # XXX unless the fields are changing often this is wrong
        ('Pragma', 'no-cache') 
    ])
    return template.render(fields=fields)


def env(environ, start_response):

    from pprint import pformat

    start_response('200 OK', [('Content-Type', 'text/plain')])
    return [pformat(environ)]


def register(environ, start_response):
    query = environ['tiddlyweb.query']
    name = query.get('name', [None])[0]
    company = query.get('company', [None])[0]
    country = query.get('country', [None])[0]
    email = query.get('email', [None])[0]
    if not (name and company and email):
        # The form has not been filled out
        raise HTTP302(server_base_url(environ) + '/pages/register.html')
    to_address = environ['tiddlyweb.config'].get(
            'wikidata.register_address', 'cdent@peermore.com')
    subject = 'Registration Request'
    body = """
name: %s
email: %s
company: %s
country: %s
""" % (name, email, company, country)
    try:
        send_email(to_address, subject, body)
    except socket.error:
        logging.debug('failed to send: %s:%s:%s', to_address, subject, body)
    raise HTTP303(server_base_url(environ) + '/pages/registered.html')

    
def verify(environ, start_response):

    logging.debug(environ['tiddlyweb.query'])
    try:
        redirect = environ['tiddlyweb.query']['recaptcha_redirect'][0]
    except (KeyError, IndexError):
        redirect = environ['HTTP_REFERER'].split('?', 1)[0]
    commonVars = templating.common_vars(environ)
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
    
        resp = captcha.submit(challenge_field, response_field, private_key, ip_addr)
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
    
    return []


@require_role('ADMIN')
def tier2_user_form(environ, start_response):
    return _user_form(environ, start_response, role='tier2')


def _user_form(environ, start_response, role='tier1', message='', formdata=None):
# XXX add an action argument so we can choose if we are doing tier1
# or tier2 registration
    form_starter = {
            'name': '',
            'email': '',
            'country': '',
            'company': '',
            }
    if formdata:
        form_starter.update(formdata)

    if role == 'tier2':
        template = templating.get_template(environ, 'user_form.html')
    else:
        template = templating.get_template(environ, 'user_self_form.html')

    start_response('200 OK', [
        ('Content-Type', 'text/html'),
        ('Pragma', 'no-cache')
        ])
    
    return template.render(commonVars=templating.common_vars(environ),
            message=message, form=form_starter)


def create_tier1_user(environ, start_response):
    """
    This is improper and insecure.
    """
    query = environ['tiddlyweb.query']
    now = time.time()
    expiration = now + (DEFAULT_EXPIRE_DAYS * 24 * 60 * 60)
    return _create_user(environ, start_response, expiration=expiration,
            role='tier1')


@require_role('ADMIN')
def create_tier2_user(environ, start_response):
    """
    This is improper and insecure.
    """
    query = environ['tiddlyweb.query']
    now = time.time()
    expiration = query.get('expiration', [90])[0] # days
    expiration = now + (expiration * 24 * 60 * 60)
    return _create_user(environ, start_response, creation=now,
            expiration=expiration, role='tier2')

def _create_user(environ, start_response, creation=0, expiration=0, role='tier1'):
    if creation == 0:
        creation = time.time()
    store = environ['tiddlyweb.store']
    query = environ['tiddlyweb.query']
    name = query.get('name', [None])[0]
    email = query.get('email', [None])[0]
    company = query.get('company', [None])[0]
    country = query.get('country', [None])[0]
    if not (name and email):
        # The form has not been filled out
        return _user_form(environ, start_response, role=role, message='Missing Data!',
                formdata={'name': name, 'email': email,
                    'company': company, 'country': country})
    user = User(email)
    try:
        user = store.get(user)
        # User exists!
        return _user_form(environ, start_response, role=role, message='That user already exists!',
                formdata={'name': name, 'email': email,
                    'company': company, 'country': country})
    except NoUserError:
        password = _random_pass()
        user.set_password(password)
        user.add_role(role)
        store.put(user)

    bag_name = environ['tiddlyweb.config'].get('magicuser.bag', 'MAGICUSER')
    ensure_bag(bag_name, store, policy_dict={
        'read': ['NONE'], 'write': ['NONE'],
        'create': ['NONE'], 'manage': ['NONE']})
    tiddler = Tiddler(email, bag_name)
    tiddler.fields['country'] = country
    tiddler.fields['company'] = company
    tiddler.fields['name'] = name
    # Set the creation and expiration times.
    now = time.time()
    tiddler.fields['creation'] = '%s' % creation
    tiddler.fields['expiry'] = '%s' % expiration
    store.put(tiddler)

    to_address = email
    subject = "Wiki-Data user info"
    body = """
Here's your info:
Username: %s
Password: %s
""" % (email, password)
    query_string = '?email=%s' % to_address
    try:
        send_email(to_address, subject, body)
        query_string += '&success=1&role=%s' % role
        raise HTTP303(server_base_url(environ)+'/pages/new_account'+query_string)
    except socket.error:
        logging.debug('failed to send: %s:%s:%s', to_address, subject, body)
        query_string += '&failure=1&role=%s' % role
        raise HTTP302(server_base_url(environ)+'/pages/new_account'+query_string)


def _random_pass():
    import string
    from random import choice
    chars = string.letters + string.digits
    stuff = ''.join([choice(chars) for i in xrange(8)])
    return stuff


def init(config):
    merge_config(config, local_config)
    tiddlywebplugins.magicuser.init(config)
    tiddlywebplugins.jsonp.init(config)

    if 'selector' in config:
        tiddlywebplugins.logout.init(config)

        config['selector'].add('/pages/{template_file:segment}',
                GET=template_route)
        config['selector'].add('/test/{template_file:segment}',
                GET=test_template_route)
        config['selector'].add('/index.html', GET=index)
        config['selector'].add('/verify', POST=verify)
        config['selector'].add('/lib/fields.js', GET=get_fields_js)
        config['selector'].add('/env', GET=env)
        config['selector'].add('/register', POST=register)
        config['selector'].add('/_admin/createuser', GET=tier2_user_form, POST=create_tier2_user)
        config['selector'].add('/createuser', POST=create_tier1_user)
        replace_handler(config['selector'], '/', dict(GET=index))
        remove_handler(config['selector'], '/recipes')
        remove_handler(config['selector'], '/recipes/{recipe_name}')
        remove_handler(config['selector'], '/recipes/{recipe_name}/tiddlers')
        remove_handler(config['selector'], '/bags')
        remove_handler(config['selector'], '/bags/{bag_name}')
        remove_handler(config['selector'], '/bags/{bag_name}/tiddlers')
