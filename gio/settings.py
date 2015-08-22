# coding: utf-8
import os
import sys

BASE_DIR = os.path.dirname(__file__)
EXTRA_DIR = os.path.dirname(BASE_DIR)

sys.path.append(EXTRA_DIR)

DEBUG = False
SECRET_KEY = 'qidmmkj#wb-13l_$4_cmozv)g4te3v&di6@@c&(xkbomxwlyfv'


try:
    from settings_local import *
except ImportError:
    pass
