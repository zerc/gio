# coding: utf-8
import pprint
import importlib

import requests

from app import app

from .db import QueueItem

__ALL__ = ('AdaptersRouter', 'PPrint')


class AdaptersRouter(object):
    """ Router for selected adapters.
    """
    def __init__(self):
        a_strings = app.config.get('GIO_TARGET_ADAPTERS', None)
        if not a_strings:
            raise AttributeError(
                'You must specify minimum one adapter for delivery')

        self._adapters = []

        for path in a_strings:
            args = tuple()

            if isinstance(path, tuple):
                path, args = path

            try:
                module, cls = path.rsplit('.', 1)
            except ValueError:
                raise ValueError('Adapter must by inside some module')

            self._adapters.append(
                getattr(importlib.import_module(module), cls)(*args))

    def process(self):
        while True:
            item = QueueItem.find_one_for_sending()
            if not item:
                break

            for a in self._adapters:
                a.process(item)


class BaseAdapter(object):
    """ Common class for delivery adapters.
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def process(self, item):
        raise NotImplementedError('You must implement .process method')


class PPrint(BaseAdapter):
    """ Just prints payload to stdout.
    """
    def __init__(self, *args, **kwargs):
        super(PPrint, self).__init__(*args, **kwargs)
        self.pp = pprint.PrettyPrinter(indent=4)

    def process(self, item):
        self.pp.pprint(item)


class Remote(BaseAdapter):
    """ Send json data to 3rd parth system.
    """
    def __init__(self, url, *args, **kwargs):
        self.url = url
        self.headers = {
            'Content-Type': 'application/json'
        }

    def process(self, item):
        requests.post(self.url, data=item, headers=self.headers)
