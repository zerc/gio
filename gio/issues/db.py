# coding: utf-8
from app import db

# For this time we just setting up collection without defining Document it
# because i don't want worry about data validation, transformation to other
# format etc.
# But typically define the Document model it very right idea.
issues = db.issues
events = db.events


def safe_fetch(coll, *args, **kwargs):
    """ Wrapper around .find method for skipping some staff keys.
    """
    for item in coll.find(*args, **kwargs):
        yield _safe(item)


def get_one_or_none(coll, *args, **kwargs):
    """ Wrapper for getting one element from collection.
    """
    return _safe(coll.find_one(*args, **kwargs))


def _safe(item):
    """ Hide some staff property.
    """
    if not item:
        return item

    UNSAFE = ('_id', '_issue_number')
    return {k: v for k, v in item.items() if k not in UNSAFE}
