# coding: utf-8
from flask import Flask
from flask.ext.script import Manager

from github import Github
from pymongo import MongoClient

app = Flask(__name__,
            instance_relative_config=True)

app.config.from_object('settings')

manager = Manager(app)
mongo = MongoClient(app.config['MONGO_HOST'], app.config['MONGO_PORT'])
db = getattr(mongo, __name__)

gh = Github(app.config['GIO_APP_TOKEN'])
repo = gh.get_repo(app.config['GIO_WATCHED_REPO'])


def setup(app):
    from issues import issues_app

    app.register_blueprint(issues_app)


setup(app)
