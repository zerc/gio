# coding: utf-8
from flask import Blueprint, abort
from flask_restful import Resource, Api

from .db import issues, events, safe_fetch, get_one_or_none

issues_app = Blueprint('issues', __name__)
api = Api(issues_app)


@issues_app.route('/')
def index():
    return u'Hello world'


@api.resource('/issues/')
class IssuesResource(Resource):
    """ REST methods for fetching issues.
    """
    def get(self):
        result = safe_fetch(issues)
        # In real life application i must process pagination of course
        return list(result)


@api.resource('/issues/<int:issue_number>/')
class IssueDetailResource(Resource):
    """ Fetch one issue. Just tradition.
    """
    def get(self, issue_number):
        result = get_one_or_none(issues, {'number': issue_number})
        if result:
            return result
        raise abort(404)


@api.resource('/issues/<int:issue_number>/events/')
class EventsResourse(Resource):
    """ List events for selected issue.
    """
    def get(self, issue_number):
        result = safe_fetch(events, {'_issue_number': issue_number})
        return list(result)
