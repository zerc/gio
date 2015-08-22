GIO - Github Issues Observer
============================

This micro service will accept all webhook from Github and dispatch to the target system. In most case, it will just replay the request from Github.

In addition, it will:

* pull the issue event stream: https://developer.github.com/v3/issues/events/.
* pull the GET /repos/:owner/:repo/issues https://developer.github.com/v3/issues/.
* composes a push webhook to the target system when issues description or title updated. To simulate Github Webhook of issue description and title update.

Install
-------


Usage
-----
