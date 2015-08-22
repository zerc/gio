# coding: utf-8
from flask.ext.script import Command
from app import repo, manager

from .db import Event, Issue


class BasePullCommand(Command):
    """ Base class for pull-based commands
    """
    def run(self, since=None):
        """ Fetching issues and his events from Github.

        :since: If provided then fetch issues starts from this.
        """
        issues = repo.get_issues()

        for i in issues:
            self.proccess_issue(i)

            for e in i.get_events():
                self.proccess_event(e, i)

    def proccess_issue(self, issue):
        return Issue.insert_or_update(issue.raw_data)

    def proccess_event(self, event, issue):
        return Event.insert_or_update(
            event.raw_data,
            extra={'issue_number': issue.number})


class PullCommand(BasePullCommand):
    """ Pull issues and events from Github repository.
    """


manager.add_command('pull', PullCommand())


@manager.command
def drop_data():
    Event.drop()
    Issue.drop()
