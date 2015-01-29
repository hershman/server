"""
The Flask frontend for the GA4GH API.

TODO Document properly.
"""
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import os
import flask
import flask.ext.api as api
from flask.ext.api.decorators import set_renderers
import flask.ext.cors as cors

app = flask.Flask(__name__) #api.FlaskAPI
app.config.from_object('ga4gh.server.config:DefaultConfig')
if os.environ.get('GA4GH_CONFIGURATION') is not None:
    app.config.from_envvar('GA4GH_CONFIGURATION')

cors.CORS(app, allow_headers='Content-Type')

def handleHTTPGet(request, endpoint):
    """
    Handles the specified HTTP POST request, which maps to the specified
    protocol handler handpoint and protocol request class.
    """
    mimetype = "application/json"
    responseStr = endpoint(request)
    return flask.Response(responseStr, status=200, mimetype=mimetype)


def handleHTTPPost(request, endpoint):
    """
    Handles the specified HTTP POST request, which maps to the specified
    protocol handler handpoint and protocol request class.
    """
    mimetype = "application/json"
    if request.mimetype != mimetype:
        raise api.exceptions.UnsupportedMediaType()
    responseStr = endpoint(request.get_data())
    return flask.Response(responseStr, status=200, mimetype=mimetype)


def handleHTTPOptions():
    """
    Handles the specified HTTP OPTIONS request.
    """
    response = flask.Response("", mimetype="application/json")
    response.headers.add("Access-Control-Request-Methods", "GET,POST,OPTIONS")
    return response


@app.route('/')
def index():
    if app.config["BEACON"]:
        return flask.render_template('beaconClient.html', variant_sets=["1kg_phase3"])
    else:
        flask.abort(404)


if app.config["BEACON"]:
    @app.route('/info', methods=["GET"])
    def infoBeacon():
         return handleHTTPGet(flask.request, app.backend.infoBeacon)

    @app.route('/query', methods=["GET"])
    def queryBeacon():
         return handleHTTPGet(flask.request, app.backend.searchBeacon)

@app.route('/references/<id>', methods=['GET'])
def getReference(id):
    flask.abort(404)


@app.route('/references/<id>/bases', methods=['GET'])
def getReferenceBases(id):
    flask.abort(404)


@app.route('/referencesets/<id>', methods=['GET'])
def getReferenceSet(id):
    flask.abort(404)


@app.route('/callsets/search', methods=['POST'])
def searchCallSets():
    flask.abort(404)


@app.route('/readgroupsets/search', methods=['POST'])
def searchReadGroupSets():
    flask.abort(404)


@app.route('/reads/search', methods=['POST'])
def searchReads():
    flask.abort(404)


@app.route('/referencesets/search', methods=['POST'])
def searchReferenceSets():
    flask.abort(404)


@app.route('/references/search', methods=['POST'])
def searchReferences():
    flask.abort(404)


@app.route('/variantsets/search', methods=['POST', 'OPTIONS'])
def searchVariantSets():
    if flask.request.method == "POST":
        return handleHTTPPost(flask.request, app.backend.searchVariantSets)
    else:
        return handleHTTPOptions()


@app.route('/variants/search', methods=['POST', 'OPTIONS'])
def searchVariants():
    if flask.request.method == "POST":
        return handleHTTPPost(flask.request, app.backend.searchVariants)
    else:
        return handleHTTPOptions()
