"""
Map the mappingsql store into the wikidata namespace
for future expansion.
"""

import logging

from tiddlyweb.model.policy import ForbiddenError, UserRequiredError
from tiddlyweb.store import NoTiddlerError

from tiddlywebplugins.wikidata.wdsql import (Store as MappingSQLStore,
        sTiddler)

from tiddlywebplugins.mappingsql import NoResultFound



class Store(MappingSQLStore):
    """
    A MAD specific subclass of the wdsql store. This provides
    special query access as in wdsql, but also user level access
    control in search and tiddler_get.
    """

    def _determine_user_access(self):
        """
        For now we return true if the user is authenticated.
        """
        try:
            current_user = self.environ['tiddlyweb.usersign']
        except KeyError:
            return False
        if current_user['name'] == u'GUEST':
            raise UserRequiredError('A login is required for this action.')
        if 'tier2' in current_user['roles']:
            return 2
        if 'tier1' in current_user['roles']:
            return 1
        raise ForbiddenError('Tiered access required for this action.')

    def tiddler_get(self, tiddler):
        """
        Get tiddlers with limited view on the fields.
        """
        full_access = self._determine_user_access()
        open_fields = self.environ[
                'tiddlyweb.config'].get(
                        'mappingsql.open_fields', [])
        self._validate_bag_name(tiddler.bag)
        try:
            if full_access == 1:
                stiddler = (self.session.query(sTiddler).filter(
                    getattr(sTiddler, self.id_column) == tiddler.title)
                    .filter(sTiddler.taster == 'Y').one())
            elif full_access == 2:
                stiddler = (self.session.query(sTiddler).filter(
                    getattr(sTiddler, self.id_column) == tiddler.title).one())
            else:
                raise ForbiddenError('incorrect user access')
        except NoResultFound, exc:
            raise NoTiddlerError('tiddler %s not found, %s' %
                    (tiddler.title, exc))
        # now we need to map the sTiddlers columns to a tiddler
        columns = stiddler.__dict__.keys()
        columns.remove(self.id_column)
        for column in columns:
            if column.startswith('_'):
                continue
            if open_fields and column not in open_fields:
                continue
            if hasattr(tiddler, column):
                setattr(tiddler, column, unicode(getattr(stiddler, column)))
            else:
                tiddler.fields[column] = unicode(getattr(stiddler, column))
        if not tiddler.text:
            tiddler.text = ''
        return tiddler

    def run_query(self, query, branches, full_access, slice_index):
        """
        Run the query, modified by access controls.
        """
        limit = self.environ['tiddlyweb.config'].get(
                'mappingsql.limit', 50)
        if not branches:
            query = query.filter(
                    sTiddler.entity_type != 'SLE').filter(
                            sTiddler.entity_type != 'BRA')
        count = query.count()
        logging.debug('count is: %s', count)
        self.environ['tiddlyweb.mappingsql.count'] = count
        if full_access == 1:
            query = query.filter(sTiddler.taster == 'Y')
        access_count = query.count()
        logging.debug('access_count is: %s', access_count)
        self.environ['tiddlyweb.mappingsql.access_count'] = access_count
        logging.debug('query is: %s', query)
        return query.slice(slice_index, slice_index + limit).all()

    def process_fields(self, query, fields, full_access):
        """
        Add to the query for fields on which we are searching.
        """
        open_fields = self.environ['tiddlyweb.config'].get(
                'mappingsql.open_fields', [])
        have_query = False
        for field in fields:
            if open_fields and field not in open_fields:
                continue
            terms = fields[field]
            # TODO: For now we only accept the first term provided
            query = query.filter(getattr(sTiddler, field) == terms[0])
            have_query = True
        return query, have_query
