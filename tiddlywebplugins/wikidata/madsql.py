"""
Map the mappingsql store into the wikidata namespace
for future expansion.
"""

from tiddlywebplugins.mappingsql import Store


class Store(MappingSQLStore):
    
    def tiddler_get(self, tiddler):
        full_access = self._determine_user_access()
        open_fields = self.environ[
                'tiddlyweb.config'].get(
                        'mappingsql.open_fields', [])
        tasters = self.environ[
                'tiddlyweb.config'].get(
                        'mappingsql.tasters', False)
        self._validate_bag_name(tiddler.bag)
        try:
            if tasters and not full_access:
                stiddler = self.session.query(sTiddler).filter(
                        getattr(sTiddler, self.id_column)==tiddler.title).filter(
                                sTiddler.taster=='Y').one()
            else:
                stiddler = self.session.query(sTiddler).filter(
                        getattr(sTiddler, self.id_column)==tiddler.title).one()
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

    def search(self, search_query=''):
        full_access = self._determine_user_access()
        logging.debug('full_access: '+str(full_access))
        open_fields = self.environ[
                'tiddlyweb.config'].get(
                        'mappingsql.open_fields', [])

        query = self.environ.get('tiddlyweb.query', {})
        try:
            slice_index = int(query['index'][0])
            del query['index']
            self.environ['tiddlyweb.mappingsql.index'] = slice_index
        except KeyError:
            slice_index = 0

        query_string, fields = query_dict_to_search_tuple(
                self.environ.get('tiddlyweb.query', {}))

        query = self.session.query(getattr(sTiddler, self.id_column))
        have_query = False

        if query_string:
            if self.environ['tiddlyweb.config'].get('mappingsql.full_text', False):
                query = query.filter(
                                'MATCH(%s) AGAINST(:query in boolean mode)' %
                                ','.join(
                                    self.environ['tiddlyweb.config']
                                    ['mappingsql.default_search_fields'])
                                ).params(query=query_string)
            else:
                # XXX: id and modifier fields are not guaranteed to be
                # present. i.e. this code is wrong!
                query = query.filter(or_(
                            sTiddler.id.like('%%%s%%' % query_string),
                            sTiddler.modifier.like('%%%s%%' % query_string)))
            have_query = True

        for field in fields:
            if open_fields and field not in open_fields:
                continue
            terms = fields[field]
            # TODO: For now we only accept the first term provided
            query = query.filter(getattr(sTiddler, field)==terms[0])
            have_query = True

        count = 0
        if have_query:
            limit = self.environ['tiddlyweb.config'].get('mappingsql.limit', 50)
            count = query.count()
            logging.debug('count is: %s', count)
            self.environ['tiddlyweb.mappingsql.count'] = count
            tasters = self.environ[
                'tiddlyweb.config'].get(
                        'mappingsql.tasters', False)
            if tasters and not full_access:
                query = query.filter(sTiddler.taster=='Y')
            access_count = query.count()
            logging.debug('access_count is: %s', access_count)
            self.environ['tiddlyweb.mappingsql.access_count'] = access_count
            logging.debug('query is: %s', query)
            stiddlers = query.slice(slice_index, slice_index + limit).all()
        else:
            stiddlers = []

        bag_name = self.environ['tiddlyweb.config']['mappingsql.bag']
        tiddlers =  (Tiddler(
            unicode(getattr(stiddler, self.id_column)), bag_name)
            for stiddler in stiddlers)

        return tiddlers
