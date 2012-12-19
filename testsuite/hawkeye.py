from unittest.runner import TextTestRunner
from tests import datastore_tests

__author__ = 'hiranya'

if __name__ == '__main__':
  suite = datastore_tests.suite()
  TextTestRunner(verbosity=2).run(suite)