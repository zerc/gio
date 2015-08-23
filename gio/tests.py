# coding: utf-8
import os
import unittest

if __name__ == "__main__":
    # Yes dirty hack but it solving of many problems
    try:
        os.environ['GIO_TEST'] = 'test'
        from app import app
        suite = unittest.loader.TestLoader().discover(app.config['BASE_DIR'])
        unittest.TextTestRunner(verbosity=2).run(suite)
    finally:
        del os.environ['GIO_TEST']
