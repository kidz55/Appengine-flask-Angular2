"""`main` is the top level module for your Flask application."""
from flask import jsonify, request
from collections import defaultdict
from .query import query_from_bigquery, query_async_from_bigquery
from application import app

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



