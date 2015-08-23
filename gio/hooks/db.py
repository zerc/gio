# coding: utf-8
from app import db, app, signals, repo, gh_user

from core import BaseItem
from issues.db import issue_updated, Issue, EventTypes

__ALL__ = ('QueueItem',)


class QueueItemClass(BaseItem):
    """ Queue from items ready to sending.
    """
    coll = db.hooks_queue

    def insert(self, item, **kwargs):
        kwargs.setdefault('extra', {}).update({
            'sended': False,
        })
        return super(QueueItemClass, self).insert(item, **kwargs)

    def find_one_for_sending(self):
        """ Find item for sending. Mark him as sended and return.
        More better way - setting this flag only if data successfully sended.
        """
        return self._safe(self.coll.find_one_and_update(
            {'_gio_data.sended': False},
            {'$set': {'_gio_data.sended': True}}))


QueueItem = QueueItemClass()


@issue_updated.connect_via(Issue)
def create_hook(sender, new_item, old_item):
    """ Create hook for updated issue.
    """
    data = {
        'action': EventTypes.UPDATED,
        'issue': new_item,
        'repository': repo.raw_data,
        'sender': gh_user.raw_data
    }
    QueueItem.insert(data)
