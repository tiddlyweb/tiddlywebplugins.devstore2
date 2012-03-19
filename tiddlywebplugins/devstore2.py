"""
experimenting with a wrapper store for dev.

This assumes that the wrapped store has references to the tiddlers
in src, thus can list_bag_tiddlers correctly.
"""

import os

from tiddlyweb.web.util import encode_name
from tiddlyweb.store import Store as StoreBoss
from tiddlyweb.stores import StorageInterface

from tiddlywebplugins.twimport import url_to_tiddler

from urllib2 import URLError

KNOWN_EXTENSIONS = ['', '.tid', '.js']


class Store(StorageInterface):

    def __init__(self, store_config=None, environ=None):
        super(Store, self).__init__(store_config, environ)
        self.config = environ.get('tiddlyweb.config', {})
        self._base = store_config['devstore_root']

        wrapped_store = StoreBoss(self.config['wrapped_devstore'][0],
                self.config['wrapped_devstore'][1], environ=environ)
        self.wrapped_storage = wrapped_store.storage

    # XXX do this automagic?
    def list_recipes(self):
        return self.wrapped_storage.list_recipes()

    def list_bags(self):
        return self.wrapped_storage.list_bags()

    def list_bag_tiddlers(self, bag):
        return self.wrapped_storage.list_bag_tiddlers(bag)

    def list_users(self):
        return self.wrapped_storage.list_users()

    def list_tiddler_revisions(self):
        return self.wrapped_storage.list_tiddler_revisions()

    def search(self, search_query):
        return self.wrapped_storage.search(search_query)

    def user_get(self, user):
        return self.wrapped_storage.user_get(user)

    def user_put(self, user):
        return self.wrapped_storage.user_put(user)

    def user_delete(self, user):
        return self.wrapped_storage.user_delete(user)

    def recipe_get(self, recipe):
        return self.wrapped_storage.recipe_get(recipe)

    def recipe_put(self, recipe):
        return self.wrapped_storage.recipe_put(recipe)

    def recipe_delete(self, recipe):
        return self.wrapped_storage.recipe_delete(recipe)

    def bag_get(self, bag):
        return self.wrapped_storage.bag_get(bag)

    def bag_put(self, bag):
        return self.wrapped_storage.bag_put(bag)

    def bag_delete(self, bag):
        return self.wrapped_storage.bag_delete(bag)

    def tiddler_put(self, tiddler):
        return self.wrapped_storage.tiddler_put(tiddler)

    def tiddler_delete(self, tiddler):
        return self.wrapped_storage.tiddler_delete(tiddler)

    def tiddler_get(self, tiddler):
        """
        do something magical with twimport/instancer here.
        """
        dev_tiddler = self._get_tiddler(tiddler)
        if not dev_tiddler:
            return self.wrapped_storage.tiddler_get(tiddler)
        return dev_tiddler

    def _get_tiddler(self, tiddler):
        bag = tiddler.bag
        filepath = os.path.join(self._base, encode_name(tiddler.bag),
                encode_name(tiddler.title))
        found = False
        index = 0
        while not found:
            try:
                extension = KNOWN_EXTENSIONS[index]
            except IndexError:
                return None
            try:
                tiddler = url_to_tiddler(filepath + extension)
                found = True
            except URLError:
                index += 1
        tiddler.bag = bag
        return tiddler
