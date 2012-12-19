import json
from unittest.suite import TestSuite
from hawkeye_test_case import HawkeyeTestCase

__author__ = 'hiranya'

class SimpleKindAwareInsertTest(HawkeyeTestCase):
  def runTest(self):
    response = self.http_post('/datastore/project', 'name=Synapse&description=Mediation Engine')
    dict = json.loads(response.read())
    self.assertEquals(response.status, 200)
    self.assertTrue(dict['id'] is not None)

    response = self.http_post('/datastore/project', 'name=Xerces&description=XML Parser')
    dict = json.loads(response.read())
    self.assertEquals(response.status, 200)
    self.assertTrue(dict['id'] is not None)

class KindAwareInsertWithParentTest(HawkeyeTestCase):
  def runTest(self):
    response = self.http_get('/datastore/project')
    project_list = json.loads(response.read())
    self.assertTrue(len(project_list) > 0)
    projects = []
    for entry in project_list:
      projects.append(json.loads(entry)['id'])

    response = self.http_post('/datastore/module',
      'name=Core&description=Mediation Core&project_id=' + projects[0])
    dict = json.loads(response.read())
    self.assertEquals(response.status, 200)
    self.assertTrue(dict['id'] is not None)

    response = self.http_post('/datastore/module',
      'name=NHTTP&description=NIO HTTP transprot&project_id=' + projects[0])
    dict = json.loads(response.read())
    self.assertEquals(response.status, 200)
    self.assertTrue(dict['id'] is not None)

class SimpleKindAwareQueryTest(HawkeyeTestCase):
  def runTest(self):
    response = self.http_get('/datastore/project')
    project_list = json.loads(response.read())
    self.assertTrue(len(project_list) > 0)
    for entry in project_list:
      project_dict = json.loads(entry)
      response = self.http_get('/datastore/project?id=' + project_dict['id'])
      list = json.loads(response.read())
      dict = json.loads(list[0])
      self.assertEquals(len(list), 1)
      self.assertEquals(dict['name'], project_dict['name'])

    response = self.http_get('/datastore/module')
    module_list = json.loads(response.read())
    self.assertTrue(len(module_list) > 0)
    for entry in module_list:
      module_dict = json.loads(entry)
      response = self.http_get('/datastore/module?id=' + module_dict['id'])
      list = json.loads(response.read())
      dict = json.loads(list[0])
      self.assertEquals(len(list), 1)
      self.assertEquals(dict['name'], module_dict['name'])

class AncestorQueryTest(HawkeyeTestCase):
  def runTest(self):
    response = self.http_get('/datastore/project')
    project_list = json.loads(response.read())
    self.assertTrue(len(project_list) > 0)
    projects = {}
    for entry in project_list:
      project_id = json.loads(entry)['id']
      response = self.http_get('/datastore/project_modules?project_id=' + project_id)
      entity_list = json.loads(response.read())
      if len(entity_list) > 1:
        modules = []
        project = None
        for entity in entity_list:
          dict = json.loads(entity)
          if dict['type'] == 'project':
            project = dict['name']
          elif dict['type'] == 'module':
            modules.append(dict['name'])
        projects[project] = modules
    self.assertTrue(len(projects) > 0)
    self.assertTrue(projects['Synapse'].index('Core') != -1)
    self.assertTrue(projects['Synapse'].index('NHTTP') != -1)


def suite():
  suite = TestSuite()
  suite.addTest(SimpleKindAwareInsertTest())
  suite.addTest(KindAwareInsertWithParentTest())
  suite.addTest(SimpleKindAwareQueryTest())
  suite.addTest(AncestorQueryTest())
  return suite


