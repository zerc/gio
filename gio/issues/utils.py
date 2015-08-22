# coding: utf-8
from app import repo

from .db import events as events_collection, issues as issues_collection


def pull(since=False):
    """ Fetching issues and his events from Github.

    :since: If provided then fetch issues starts from this.
    """
    issues = repo.get_issues()

    for i in issues:
        insert_or_update(issues_collection, i)

        for e in i.get_events():
            insert_or_update(events_collection, e, _issue_number=i.number)


def insert_or_update(coll, item, **extra):
    """ Wrapper around `collection.find_one_and_update` method.
    """
    data = item.raw_data
    data.update(extra)
    return coll.find_one_and_update(
        {'id': item.id}, {'$set': data}, upsert=True)
