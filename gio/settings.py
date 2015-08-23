# coding: utf-8
import os
import sys

BASE_DIR = os.path.dirname(__file__)
EXTRA_DIR = os.path.dirname(BASE_DIR)

sys.path.append(EXTRA_DIR)

DEBUG = False
SECRET_KEY = 'qidmmkj#wb-13l_$4_cmozv)g4te3v&di6@@c&(xkbomxwlyfv'

# Flask-PyMongo currently not support PyMongo > 3 version and i dont using it
MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'gio'

# === Project specific settings ===
# You can obtain it here: https://github.com/settings/tokens
# If not set - do requests as anonymous user who has hard rate limits
GIO_APP_TOKEN = None

# Format: owner/repo
GIO_WATCHED_REPO = 'zerc/django-vest'

# Secret string
GIO_HOOKS_SECRET = None

# List of 3rd adapters used for deliver events
GIO_TARGET_ADAPTERS = (
    'hooks.adapters.PPrint',
)


try:
    from settings_local import *
except ImportError:
    pass
