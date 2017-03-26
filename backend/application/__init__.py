from google.cloud import bigquery
from flask import Flask
from flask_cors import CORS
from google.appengine.api import urlfetch

app = Flask('application')
CORS(app)
bq = bigquery.Client()
urlfetch.set_default_fetch_deadline(60)

from application import views, query