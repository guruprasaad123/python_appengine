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
import cgi
import os
import datetime
import webapp2
import logging
import json
from handler import data_handler
from google.appengine.ext import ndb
from google.appengine.api import users
from google.appengine.api import search
from google.appengine.ext.webapp import template


guestbook_key = ndb.Key('Guestbook', 'default_guestbook')

class Greeting(ndb.Model):
  author = ndb.UserProperty()
  content = ndb.TextProperty()
  date = ndb.DateTimeProperty(auto_now_add=True)

class Search(webapp2.RequestHandler):
  def post(self):
    response_data={}
    json_request = json.loads(self.request.body)
    search_for = json_request['search'];
    search_analysis = search.Index('ANALYSIS_CASELETS')
    search_results = search_analysis.search(search_for)
    number_found  = search_results.number_found
    field_results=[]
    for result in search_results:
      obj={}
      for field in result.fields:
        obj[field.name]=field.value
      field_results.append(obj)

    response_data['number']=number_found
    response_data['data']=field_results
    response_data['searchFor']=search_for
    self.response.out.write(json.dumps(response_data))

  def get(self):
    values={
      'head':'Search',
      'sample':'searching',
    }
    path = os.path.join(os.path.dirname(__file__),'template' ,'search.html')
    self.response.out.write(template.render(path,values))

class Analysis(webapp2.RequestHandler):
  def get(self):
    self.response.headers['Access-Control-Allow-Methods']='*'
    self.response.headers['Access-Control-Allow-Headers']='*'
    #self.response.headers['Accept']='application/json'
    self.response.out.write('<html><body>')
    analysis_handler = data_handler()
    results=analysis_handler.modelize()
    if(results is None):
      self.response.out.write("""
      <ul><li>
      No Results Data
      </li></ul>
      """)
    else:
      self.response.out.write('<ol>')
      for X in results:
        self.response.out.write('<li> %s </li>' % X[0].id)
      self.response.out.write('</ol>')
    self.response.out.write("""
    </body></html>
    """)



class MainPage(webapp2.RequestHandler):
  def get(self):
    self.response.out.write('<html><body>')

    greetings = ndb.gql('SELECT * '
                        'FROM Greeting '
                        'WHERE ANCESTOR IS :1 '
                        'ORDER BY date DESC LIMIT 10',
                        guestbook_key)

    for greeting in greetings:
      if greeting.author:
        self.response.out.write('<b>%s</b> wrote:' % greeting.author.nickname())
      else:
        self.response.out.write('An anonymous person wrote:')
      self.response.out.write('<blockquote>%s</blockquote>' %
                              cgi.escape(greeting.content))


    self.response.out.write("""
          <form action="/sign" method="post">
            <div><textarea name="content" rows="3" cols="60"></textarea></div>
            <div><input type="submit" value="Sign Guestbook"></div>
          </form>
        </body>
      </html>""")


class Guestbook(webapp2.RequestHandler):
  def post(self):
    greeting = Greeting(parent=guestbook_key)

    if users.get_current_user():
      greeting.author = users.get_current_user()

    greeting.content = self.request.get('content')
    greeting.put()
    self.redirect('/')


app = webapp2.WSGIApplication([
  ('/', MainPage),
  ('/sign', Guestbook),
  ('/analysis',Analysis),
  ('/search',Search)
], debug=True)
