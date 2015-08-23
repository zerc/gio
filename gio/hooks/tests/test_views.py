# coding: utf-8
import os
import json

from flask import url_for

from app import app

from core import BaseTestCase
from hooks.db import QueueItem


class TestViews(BaseTestCase):
    """ TestCase for collecting hooks.
    """
    def test_receiving(self):
        """ View availible and queue item created.
        """
        hook = self.get_hook()

        response = self.client.post(
            url_for('hooks.proccess_hook'),
            data=hook,
            content_type='application/json')

        self.assertEqual(response.status_code, 200)
        self.assertTrue(QueueItem.get({'issue.number': 1347}))

    def get_hook(self):
        fname = os.path.join(
            app.config['BASE_DIR'],
            'hooks', 'tests', 'fixtures', 'hook.json')

        with open(fname) as f:
            return f.read()
