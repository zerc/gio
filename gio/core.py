# coding: utf-8
""" Some common functional.
"""
import copy

from pymongo import ASCENDING

from app import app

__ALL__ = ('BaseItem',)


class BaseItem(object):
    """ Common mongodb item wrapper.
    """
    UNSAFE_ATTRS = ('_id', '_gio_data')

    coll = None

    indexes = None

    def __init__(self, *args, **kwargs):
        self.repo_name = app.config['GIO_WATCHED_REPO']
        if self.coll is None:
            raise NotImplementedError('Item subclasses must define coll attr')

        if self.indexes:
            self.coll.create_index([(i, ASCENDING) for i in self.indexes])

    def insert(self, item, **kwargs):
        data = copy.deepcopy(item)
        self.patch_meta_info(data, kwargs.pop('extra', {}))
        return self.coll.insert_one(data, **kwargs)

    def find(self, *args, **kwargs):
        """ Wrapper around .find method for skipping some staff keys.
        """
        for item in self.coll.find(*args, **kwargs):
            yield self._safe(item)

    def get(self, *args, **kwargs):
        """ Wrapper for getting one element from collection.
        """
        return self._safe(self.coll.find_one(*args, **kwargs))

    def drop(self):
        """ Drop it all
        """
        return self.coll.drop()

    def patch_meta_info(self, data, extra):
        meta_info = {
            '_gio_data': {
                'repo': self.repo_name
            }
        }
        meta_info['_gio_data'].update(extra)
        data.update(meta_info)
        return data

    def _safe(self, item):
        """ Hide some staff property.
        """
        if not item:
            return item

        return {k: v for k, v in item.items() if k not in self.UNSAFE_ATTRS}
