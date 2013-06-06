#!/usr/bin/env python
#
# Copyright 2013 Gestalt Lur.
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
import webapp2
import dbmodels
import jinja2
import os
from dbmodels import zh_user, temp_user, dead_zh_user, Count
from google.appengine.ext import db

JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {
            'zh_users_acitve': Count.user_active,
            'zh_users_dead': count.user_dead,
            'count_start_date': count_start_date,
        }

        template = JINJA_ENVIRONMENT.get_template('show_tweet.html')
        self.response.write(template.render(template_values))
    
app = webapp2.WSGIApplication([('/', MainHandler)], debug=True)
