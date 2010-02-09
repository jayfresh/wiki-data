"""
Map the mappingsql store into the wikidata namespace
so we can override _determine_user_access in a subclass.
"""

from tiddlywebplugins.mappingsql import Store as MappingSQLStore


class Store(MappingSQLStore):
    
    def _determine_user_access(self):
        return False
