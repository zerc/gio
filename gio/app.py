# coding: utf-8
import os
import sys
import unittest

from flask import Flask
from flask.ext.script import Manager

from github import Github, GithubException
from pymongo import MongoClient
from blinker import Namespace

app = Flask(__name__,
            instance_relative_config=True)


if os.environ.get('GIO_TEST', None) == 'test':
    app.config.from_object('settings_test')
else:
    app.config.from_object('settings')

manager = Manager(app)
mongo = MongoClient(app.config['MONGO_HOST'], app.config['MONGO_PORT'])
db = getattr(mongo, app.config['MONGO_DB'])
signals = Namespace()

gh = Github(app.config['GIO_APP_TOKEN'])
repo = gh.get_repo(app.config['GIO_WATCHED_REPO'])

try:
    gh_user = gh.get_user()
except GithubException.GithubException:
    class GhUser(object):
        """ Default user.
        """
        login = 'gio_bot'
        _id = -1

        @property
        def raw_data(self):
            return {'login': self.login, 'id': self._id}

    gh_user = GhUser()


def setup(app):
    from issues.views import issues_app
    from issues import utils

    from hooks.views import hooks_app
    from hooks import utils

    app.register_blueprint(issues_app)
    app.register_blueprint(hooks_app)


setup(app)
