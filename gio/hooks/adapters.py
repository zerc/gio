# coding: utf-8
import pprint
import importlib

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
                path, args = a

            try:
                module, cls = path.rsplit('.', 1)
            except ValueError:
                raise ValueError('Adapter must by inside some module')

            self._adapters.append(
                getattr(importlib.import_module(module), cls)(*args))

    def __iter__(self):
        for a in self._adapters:
            yield a


class BaseAdapter(object):
    """ Common class for delivery adapters.
    """
    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

    def __iter__(self):
        while True:
            item = QueueItem.find_one_for_sending()
            if not item:
                break

            yield item

    def proccess(self):
        raise NotImplementedError('You must implement .proccess method')


class PPrint(BaseAdapter):
    """ Just prints payload to stdout.
    """
    def __init__(self, *args, **kwargs):
        super(PPrint, self).__init__(*args, **kwargs)
        self.pp = pprint.PrettyPrinter(indent=4)

    def proccess(self):
        for item in self:
            self.pp.pprint(item)
