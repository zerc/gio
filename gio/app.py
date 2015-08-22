# coding: utf-8
from flask import Flask
from flask.ext.script import Manager

from github import Github
from pymongo import MongoClient
from blinker import Namespace

app = Flask(__name__,
            instance_relative_config=True)

app.config.from_object('settings')

manager = Manager(app)
mongo = MongoClient(app.config['MONGO_HOST'], app.config['MONGO_PORT'])
db = getattr(mongo, __name__)
signals = Namespace()

gh = Github(app.config['GIO_APP_TOKEN'])
repo = gh.get_repo(app.config['GIO_WATCHED_REPO'])


def setup(app):
    from issues import issues_app
    from issues import utils

    from hooks import hooks_app
    from hooks import utils

    app.register_blueprint(issues_app)
    app.register_blueprint(hooks_app)


setup(app)
