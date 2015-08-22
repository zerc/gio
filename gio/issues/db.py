# coding: utf-8
import copy
from hashlib import md5

from app import db, app, signals
from pymongo import ASCENDING
from pymongo.collection import ReturnDocument

__ALL__ = ('issue', 'event')


issue_updated = signals.signal('issue-updated')


class BaseItemClass(object):
    """ Base wrapper for working with collection items.
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

    def insert_or_update(self, item, **kwargs):
        """ Wrapper around `collection.find_one_and_update` method.
        """

        data = copy.deepcopy(item)

        meta_info = {
            '_gio_data': {
                'repo': self.repo_name
            }
        }
        meta_info['_gio_data'].update(kwargs.pop('extra', {}))
        data.update(meta_info)

        return self.coll.find_one_and_update(
            {'id': item['id']}, {'$set': data},
            upsert=True, return_document=ReturnDocument.BEFORE)

    def get(self, *args, **kwargs):
        """ Wrapper for getting one element from collection.
        """
        return self._safe(self.coll.find_one(*args, **kwargs))

    def find(self, *args, **kwargs):
        """ Wrapper around .find method for skipping some staff keys.
        """
        for item in self.coll.find(*args, **kwargs):
            yield self._safe(item)

    def drop(self):
        """ Drop it all
        """
        return self.coll.drop()

    def _safe(self, item):
        """ Hide some staff property.
        """
        if not item:
            return item

        return {k: v for k, v in item.items() if k not in self.UNSAFE_ATTRS}


class IssueClass(BaseItemClass):
    """ Wrapper for working with issues.
    """
    coll = db.issues
    indexes = ('_gio_data.repo',)

    @staticmethod
    def make_fingerprint(item):
        """ Constructing fingerprint of Issue.
        """
        h = md5(item['title'])
        h.update(item['body'])
        return h.hexdigest()

    def insert_or_update(self, item, **kwargs):
        """ Checking Issue's fingerprint and if it changes then send signal
        about that.
        """
        new_fprint = self.make_fingerprint(item)

        kwargs.setdefault('extra', {}).update({'fingerprint': new_fprint})
        old_item = super(IssueClass, self).insert_or_update(item, **kwargs)

        if (old_item and new_fprint != old_item['_gio_data']['fingerprint']):
            issue_updated.send(self, new_item=item, old_item=old_item)

        return old_item


class EventClass(BaseItemClass):
    """ Wrapper for working with events.
    """
    coll = db.events
    indexes = ('_gio_data.issue_number', '_gio_data.repo')


Issue = IssueClass()
Event = EventClass()


@issue_updated.connect_via(Issue)
def issue_changed(sender, new_item, old_item):
    print('>>>> CHANGED')
    print(new_item)
    print(old_item)
