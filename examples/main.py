# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Frontend for Smartsheet.

Updates gPS data through smartsheet API every 10 minutes
"""
import json
import logging
import os
from api import homepage
from flask import Flask
from flask import request
from jarvan import db
from jarvan import router

 
app = Flask(__name__)
app.debug = True


@app.before_request
def before_request():
  dir_path = os.path.dirname(os.path.realpath(__file__))
  credentials_json = open(dir_path + "/credentials.json").read()
  db.open_connection(json.loads(credentials_json))

  app.logger.addHandler(logging.StreamHandler())
  app.logger.setLevel(logging.INFO)


@app.route("/api/<module>", methods=["GET", "POST"])
@app.route("/api/<module>/<action>", methods=["GET", "POST"])
def api(module, action=None):
  return router.run(__file__, request, module, action)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def catch_all(path):
  """Get home page html.

  Returns:
    Home page HTML

  Args:
    path: catch-all path
  """
  out = homepage.run(path)
  return out

