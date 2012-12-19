import httplib
from unittest.case import TestCase

__author__ = 'hiranya'

HOST = 'localhost'
PORT = 8080
LANG = 'python'

class HawkeyeTestCase(TestCase):

  def http_get(self, path):
    return self.__make_request('GET', path)

  def http_post(self, path, payload):
    return self.__make_request('POST', path, payload)

  def __make_request(self, method, path, payload=None):
    path = "/" + LANG + path
    conn = httplib.HTTPConnection(HOST + ':' + str(PORT))
    if method == 'POST' or method == 'PUT':
      conn.request(method, path, payload)
    else:
      conn.request(method, path)
    response = conn.getresponse()
    conn.close()
    return response