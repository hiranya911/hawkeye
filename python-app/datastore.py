#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import json
import uuid
import wsgiref
from google.appengine.ext import webapp, db
import webapp2

class Project(db.Model):
  id = db.StringProperty(required=True)
  name = db.StringProperty(required=True)
  description = db.StringProperty(required=True)

class Module(db.Model):
  id = db.StringProperty(required=True)
  name = db.StringProperty(required=True)
  description = db.StringProperty(required=True)

def serialize(entity):
  dict = {'id': entity.id, 'name': entity.name, 'description': entity.description}
  if isinstance(entity, Project):
    dict['type'] = 'project'
  elif isinstance(entity, Module):
    dict['type'] = 'module'
  else:
    dict['type'] = 'unknown'
  return json.dumps(dict)

class ProjectHandler(webapp2.RequestHandler):
    def get(self):
      id = self.request.get('id')
      if id is None or id.strip() == '':
        results = db.GqlQuery("SELECT * FROM Project")
      else:
        results = db.GqlQuery("SELECT * FROM Project WHERE id = '{0}'".format(id))

      data = []
      for result in results:
        data.append(result)
      self.response.headers['Content-Type'] = "application/json"
      self.response.out.write(json.dumps(data, default=serialize))

    def post(self):
      project_id = str(uuid.uuid1())
      project = Project(id=project_id, name=self.request.get('name'),
        description=self.request.get('description'))
      project.put()
      self.response.headers['Content-Type'] = "application/json"
      self.response.out.write(json.dumps({ 'id' : project_id }))

class ModuleHandler(webapp2.RequestHandler):
  def get(self):
    id = self.request.get('id')
    if id is None or id.strip() == '':
      results = db.GqlQuery("SELECT * FROM Module")
    else:
      results = db.GqlQuery("SELECT * FROM Module WHERE id = '{0}'".format(id))

    data = []
    for result in results:
      data.append(result)
    self.response.headers['Content-Type'] = "application/json"
    self.response.out.write(json.dumps(data, default=serialize))

  def post(self):
    module_id = str(uuid.uuid1())
    project_id = self.request.get('project_id')
    project = db.GqlQuery("SELECT * FROM Project WHERE id = '{0}'".format(project_id))
    module = Module(id=module_id, name=self.request.get('name'),
      description=self.request.get('description'), parent=project[0])
    module.put()
    self.response.headers['Content-Type'] = "application/json"
    self.response.out.write(json.dumps({ 'id' : module_id }))

class ProjectModuleHandler(webapp2.RequestHandler):
  def get(self):
    project_id = self.request.get('project_id')
    projects = db.GqlQuery("SELECT * FROM Project WHERE id = '{0}'".format(project_id))
    q = db.Query()
    q.ancestor(projects[0])
    data = []
    for entity in q:
      data.append(entity)
    self.response.headers['Content-Type'] = "application/json"
    self.response.out.write(json.dumps(data, default=serialize))

application = webapp.WSGIApplication([
  ('/python/datastore/project', ProjectHandler),
  ('/python/datastore/module', ModuleHandler),
  ('/python/datastore/project_modules', ProjectModuleHandler),
], debug=True)

if __name__ == '__main__':
  wsgiref.handlers.CGIHandler().run(application)
