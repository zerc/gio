# coding: utf-8
from flask import Blueprint, abort, request

from .db import QueueItem

hooks_app = Blueprint('hooks', __name__)


@hooks_app.route('/_hooks/', methods=['POST'])
def proccess_hook():
    """ Put incoming hook into queue.
    """
    # TODO: add checking of X-Hub-Signature and X-Github-Event
    QueueItem.insert(request.json)
    return 'Ok'
