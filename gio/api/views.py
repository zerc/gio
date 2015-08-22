# coding: utf-8
from flask import Blueprint

api_app = Blueprint('api_app', __name__)


@api_app.route('/')
def index():
    return u'Hello world'
