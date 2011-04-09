"""
This is a subclass of the tiddlywebplugins.magicuser package
customized for wiki-data with the addition of expiration data.
"""

import time

from tiddlywebplugins.magicuser import Extractor as MagicExtractor

from tiddlyweb.store import StoreError
from tiddlyweb.model.tiddler import Tiddler, string_to_tags_list
from tiddlyweb.model.user import User

DEFAULT_EXPIRE_DAYS = 90

class Extractor(MagicExtractor):
    """
    Extract a user information from the HTTP request
    and then add or change the information about the
    user using tiddlers stored in some special bags.
    """

    def extract_more_info(self, environ, userinfo):
        """
        Get more information and attributes about the current
        user from a tiddler named after the user in the bag MAGICUSER.
        """
        store = environ['tiddlyweb.store']
        bag_name = environ['tiddlyweb.config'].get('magicuser.bag',
                'MAGICUSER')
        username = userinfo['name']
        tiddler = Tiddler(username, bag_name)
        try:
            tiddler = store.get(tiddler)
        except StoreError:
            pass  # tiddler is empty
        if 'roles' in tiddler.fields:
            userinfo['roles'].extend(string_to_tags_list(
                tiddler.fields['roles']))
            del tiddler.fields['roles']
        userinfo['fields'] = tiddler.fields
        userinfo['modifier'] = tiddler.modifier
        userinfo['modified'] = tiddler.modified
        userinfo['tags'] = tiddler.tags

        userinfo = self._check_expiration(environ, userinfo)

        return userinfo

    def _check_expiration(self, environ, userinfo):
        if 'expiry' not in userinfo['fields']:
            return userinfo
        expiration = float(userinfo['fields']['expiry'])
        now = time.time()

        username = userinfo['name']
        if now > expiration:
            if 'tier2' in userinfo['roles']:
                userinfo = self._downgrade_to_tier1(environ, userinfo)
            else:
                userinfo = {"name": u'GUEST', "roles": []}
                userinfo['expired_user'] = username

        return userinfo

    def _downgrade_to_tier1(self, environ, userinfo):
        store = environ['tiddlyweb.store'] 
        expiration = (time.time() + DEFAULT_EXPIRE_DAYS * 24 * 60 * 60)
        userinfo['roles'].remove('tier2')
        userinfo['roles'].append('tier1')
        userinfo['fields']['expiry'] = expiration

        bag_name = environ['tiddlyweb.config'].get('magicuser.bag', 'MAGICUSER')
        username = userinfo['name']
        tiddler = Tiddler(username, bag_name)
        try:
            tiddler = store.get(tiddler)
        except StoreError:
            pass # tiddler is empty
        tiddler.fields['expiry'] = '%s' % expiration
        store.put(tiddler)

        user = User(username)
        user = store.get(user)
        user.del_role('tier2')
        user.add_role('tier1')
        store.put(user)
        return userinfo


def init(config):
    """
    Initialize the plugin by changing configuration.
    """
    if 'tiddlywebplugins.wikidata.magicuser' not in config['extractors']:
        config['sub_extractors'] = config['extractors']
        config['extractors'] = ['tiddlywebplugins.wikidata.magicuser']
