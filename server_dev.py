#!/usr/bin/python

import argparse

from flask import Flask, request, Response
import ga4gh.protocol as protocol

from ga4gh.server import WormtableBackend, TabixBackend

# Helper function
def handleHTTPPost(request, endpoint, protocolClass):
    data = request.get_data()
    try:
        protocolRequest = protocolClass.fromJSON(data)
    except ValueError:
        return "Bad Request", 404
    protocolResponse = endpoint(protocolRequest)
    ret = protocolResponse.toJSON()
    resp = Response(response=ret,
                    status=200,
                    mimetype="application/json")
    return resp


# Globals
VariantBackend = None


# App
app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
def index():
    return "Hello world"

@app.route('/references/<id>', methods=['GET'])
def getReference(id):
    return "TODO"

@app.route('/references/<id>/bases', methods=['GET'])
def getReferenceBases(id):
    return "TODO"

@app.route('/referencesets/<id>', methods=['GET'])
def getReferenceSet(id):
    return "TODO"

@app.route('/callsets/search', methods=['POST'])
def searchCallSets():
    return "TODO"

@app.route('/readgroupsets/search', methods=['POST'])
def searchReadGroupSets():
    return "TODO"

@app.route('/reads/search', methods=['POST'])
def searchReads():
    return "TODO"

@app.route('/referencesets/search', methods=['POST'])
def searchReferenceSets():
    return "TODO"

@app.route('/references/search', methods=['POST'])
def searchReferences():
    return "TODO"

@app.route('/variantsets/search', methods=['POST'])
def searchVariantSets():
    return handleHTTPPost(request,
                          VariantBackend.searchVariantSets,
                          protocol.GASearchVariantSetsRequest)

@app.route('/variants/search', methods=['POST'])
def searchVariants():
    return handleHTTPPost(request,
                          VariantBackend.searchVariants,
                          protocol.GASearchVariantsRequest)

#### CLI
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="GA4GH reference server")
    # Add global options
    parser.add_argument(
        "--port", "-P", default=8000, type=int,
        help="The port to listen on")

    subparsers = parser.add_subparsers(title='subcommands',)

    # help
    helpParser = subparsers.add_parser(
        "help",
        description="ga4gh_server help",
        help="show this help message and exit")
    # Wormtable backend
    wtbParser = subparsers.add_parser(
        "wormtable",
        description="Serve the API using a wormtable based backend.",
        help="Serve data from tables.")
    wtbParser.add_argument(
        "dataDir",
        help="The directory containing the wormtables to be served.")
    wtbParser.set_defaults(backend=WormtableBackend)
    # Tabix
    tabixParser = subparsers.add_parser(
        "tabix",
        description="Serve the API using a tabix based backend.",
        help="Serve data from Tabix indexed VCFs")
    tabixParser.add_argument(
        "dataDir",
        help="The directory containing VCFs")
    tabixParser.set_defaults(backend=TabixBackend)

    args = parser.parse_args()
    if "backend" not in args:
        parser.print_help()
    else:
        VariantBackend = args.backend(args.dataDir)
        app.run(host='0.0.0.0', port=args.port)