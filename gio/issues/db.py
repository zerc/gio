# coding: utf-8
import copy
from hashlib import md5
from datetime import datetime

from app import db, app, signals
from core import BaseItem
from pymongo.collection import ReturnDocument

__ALL__ = ('Issue', 'Event')


issue_updated = signals.signal('issue-updated')


class BaseItemClass(BaseItem):
    """ Base wrapper for working with collection items.
    """
    coll = None

    indexes = None

    def insert_or_update(self, item, **kwargs):
        """ Wrapper around `collection.find_one_and_update` method.
        """
        data = copy.deepcopy(item)
        self.patch_meta_info(data, kwargs.pop('extra', {}))

        return self.coll.find_one_and_update(
            {'id': item['id']}, {'$set': data},
            upsert=True, return_document=ReturnDocument.BEFORE)


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


class EventTypes(object):
    UPDATED = 'updated'

Issue = IssueClass()
Event = EventClass()


@issue_updated.connect_via(Issue)
def create_event(sender, new_item, old_item):
    """ Generate event for updated issue.
    """
    event = {
        'actor': {},
        'id': None,
        'commit_id': None,
        'created_at': datetime.utcnow().isoformat(),
        'event': EventTypes.UPDATED,
        'issue': new_item
    }
    Event.insert(event, extra={'issue_number': new_item['number']})
