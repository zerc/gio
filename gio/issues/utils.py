# coding: utf-8
from datetime import datetime

from flask.ext.script import Command, Option
from github.GithubObject import NotSet

from app import repo, manager

from .db import Event, Issue, PullSession


class Puller(object):
    """ Context manager for tracking all pull sessions.
    """
    def __init__(self, force_all):
        self.kwargs = {'state': 'all'}

        if not force_all:
            self.kwargs['since'] = (PullSession.latest()
                                    or {'timestamp': NotSet})['timestamp']

    def init(self):
        """ Must be initiated inside context manager.
        """
        self.issues = repo.get_issues(**self.kwargs)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        # has exception
        if any(args):
            status = PullSession.ERROR
        else:
            status = PullSession.SUCCESS

        PullSession.insert({'status': status, 'timestamp': datetime.utcnow()})

    def proccess_issue(self, issue):
        return Issue.insert_or_update(issue.raw_data)

    def proccess_event(self, event, issue):
        return Event.insert_or_update(
            event.raw_data,
            extra={'issue_number': issue.number})


class PullCommand(Command):
    """ Pull issues and events from Github repository.
    """
    option_list = (
        Option('--force_all', '-f', dest='force_all', default=False),
    )

    def run(self, force_all):
        """ Fetching issues and his events from Github.

        :force_all: If True then fetch all issues.
        """
        with Puller(force_all) as p:
            p.init()

            for i in p.issues:
                p.proccess_issue(i)

                for e in i.get_events():
                    p.proccess_event(e, i)


manager.add_command('pull', PullCommand())


@manager.command
def drop_data():
    Event.drop()
    Issue.drop()
