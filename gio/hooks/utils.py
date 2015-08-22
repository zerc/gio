# coding: utf-8
from app import manager, app

from .adapters import AdaptersRouter


@manager.command
def send_hooks():
    """ Send stored hooks.
    """
    for ad in AdaptersRouter():
        ad.proccess()
