# coding: utf-8
from flask import url_for

from core import BaseTestCase


class TestResources(BaseTestCase):
    """ Common tests for Issues and Event resources.
    """
    TARGET_ISSUE_NUMBER = 7

    fixtures = ('issues/tests/fixtures/issues.json',
                'issues/tests/fixtures/events.json')

    def test_index(self):
        """ Index page opened.
        """
        response = self.client.get(url_for('issues.index'))
        self.assertEqual(response.status_code, 200)

    def test_issues_list(self):
        """ Issues list opened and have data
        """
        response = self.client.get(url_for('issues.issuesresource'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json)

    def test_issue_detail(self):
        """ Issue opened and have data.
        """
        response = self.client.get(url_for(
            'issues.issuedetailresource',
            issue_number=self.TARGET_ISSUE_NUMBER))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json)

    def test_invalid_detail(self):
        """ Invalid issue_number
        """
        response = self.client.get(url_for('issues.issuedetailresource',
                                           issue_number=132))
        self.assertEqual(response.status_code, 404)

    def test_events_list(self):
        """ Test events list for issue.
        """
        response = self.client.get(url_for(
            'issues.eventsresourse',
            issue_number=self.TARGET_ISSUE_NUMBER))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.json)
