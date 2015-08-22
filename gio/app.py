# coding: utf-8
from flask import Flask
from flask.ext.script import Manager


app = Flask(__name__,
            instance_relative_config=True)

app.config.from_object('settings')


def register_all(app):
    from api import api_app

    app.register_blueprint(api_app)


register_all(app)

manager = Manager(app)
