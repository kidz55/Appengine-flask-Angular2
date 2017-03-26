"""`main` is the top level module for your Flask application."""
import time, uuid
from flask import Flask, render_template, url_for, jsonify, request
from flask_cors import CORS
from google.cloud import bigquery
from google.appengine.api import urlfetch
from collections import defaultdict


app = Flask(__name__)
CORS(app)
bq = bigquery.Client()
urlfetch.set_default_fetch_deadline(60)


@app.route('/')
def index():
    """function for index."""
    json_format = defaultdict(list)
    # select 3 pictures in image database
    querystr = "SELECT original_url,title FROM `bigquery-public-data.open_images.images` LIMIT 6"
    # query to database
    url_pics = query_from_bigquery(querystr)
    # format the response into json
    for element in url_pics:
        json_format['data'].append({'url': element[0], 'title': element[1]})
    return jsonify(json_format)


@app.route('/querylabel')
def query_by_label():
    """Query a groupe of labels in database."""
    json_format = defaultdict(list)
    # data in GET methods
    label_display_name = request.args.get('label')
    # get the label names of pictures in database
    querystr = "SELECT label_display_name,label_name " \
               "FROM `bigquery-public-data.open_images.dict` " \
               "WHERE label_display_name LIKE '%{!s}%'".format(label_display_name)
    labels = query_async_from_bigquery(querystr)
    # format the response into json
    for element in labels:
        json_format['data'].append({'label': element[0], 'code': element[1]})
    return jsonify(json_format)



@app.route('/querypictures')
def query_by_label_name():
    """Query a picture by its labelname."""
    json_format = defaultdict(list)
    label_name= request.args.get('labelname')
    # get the pictures url in relation with the good label name
    querystr = "SELECT i.image_id AS image_id,original_url,title " \
               "FROM `bigquery-public-data.open_images.labels` l " \
               "INNER JOIN `bigquery-public-data.open_images.images` i " \
               "ON l.image_id = i.image_id " \
               "WHERE label_name={!s}".format(label_name)
    url_pics = query_async_from_bigquery(querystr)
    # format the response into json
    for element in url_pics:
        json_format['data'].append({'url': element[1],'title': element[2]})
    return jsonify(json_format)


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500


def query_from_bigquery(query):
    """Run query into database and return the formatted result."""
    query_results = bq.run_sync_query(query)
    # it allows to use SQL syntax
    query_results.use_legacy_sql = False
    query_results.run()
    # fetch data in row_data
    (row_data, total_rows, page_token) = query_results.fetch_data()
    return row_data


def wait_for_job(job):
    while True:
        job.reload()
        if job.state == 'DONE':
            if job.error_result:
                raise RuntimeError (job.errors)
            return
        time.sleep(1)


def query_async_from_bigquery(query):
    """Run asynchronous query into database and return the formatted result."""
    query_job = bq.run_async_query(str(uuid.uuid4()),query)
    # it allows to use SQL syntax
    query_job.use_legacy_sql = False
    query_job.begin()
    wait_for_job(query_job)
    query_results = query_job.results()

    # fetch data in row_data
    (row_data, total_rows, page_token) = query_results.fetch_data()
    return row_data


