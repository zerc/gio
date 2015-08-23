GIO - Github Issues Observer
============================

This micro service will accept all webhook from Github and dispatch to the target system. In most case, it will just replay the request from Github.

In addition, it will:

* pull the issue event stream: https://developer.github.com/v3/issues/events/.
* pull the GET /repos/:owner/:repo/issues https://developer.github.com/v3/issues/.
* composes a push webhook to the target system when issues description or title updated. To simulate Github Webhook of issue description and title update.

Dependencies
------------

Project based on Flask framework. All pythonic deps listed in `requirements.txt`. For dev purposes also i write `requirements.dev.txt` which have some useful deps for development.

Other deps:

* virutalenv - if you want using `make install` command
* mongodb - 3+ version

Install
-------

Typically after pulling this repo just type:

.. code:: shell

    $ make install

This command install virtualenv, activate it and install all python deps for us.


After that you can run tests for checking:

.. code:: shell

    $ make test

Usage
-----

First you may want to edit you local settings like this:

.. code:: shell

    $ cp settings_local.example settings_local.py

After that look at `gio/settings.py` for list of settings specified for project. Some main important:

* ``MONGO_HOST``, ``MONGO_PORT``, ``MONGO_DB`` - settings for access to MongoDB.
* ``GIO_APP_TOKEN`` - I recommend obtain it for avoiding troubles with rate limits. https://github.com/settings/tokens
* ``GIO_WATCHED_REPO`` - repo what you want observe

After configuration we can use following things.

Pulling all issues and events from ``GIO_WATCHED_REPO``. It may be long for first time.

.. code:: shell

    python gio/manage.py pull

For next time it will pull only updated data (uses `since` github api param).

For receiving webhooks use ``/_hooks/`` endpoint. Just setup you repo for it.

After webhooks received it store in queue and wait for sending. It making for minimum blocking time GitHub hooks sender (it have 30sec timeout btw) and make independent sending mechanism. And for send all hooks to 3rd system you can use:

.. code:: shell

    python gio/manage.py send_hooks


You can place calls of ``pull`` and ``send_hook`` commands to crontab in your server.
