#!/usr/bin/python

import argparse

from flask import Flask, request, Response
import ga4gh.protocol as protocol

from ga4gh.server import WormtableBackend, TabixBackend

# Globals
variant_sets = []
backend = None

# App
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello world"

def handleHTTPPost(request, endpoint, protocolClass):
    data = request.get_data() #request.get_json()
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

# TODO: OPTIONS support
@app.route('/variants/search', methods=['POST', 'OPTIONS'])
def searchVariants():
    if request.method == 'POST':
        return handleHTTPPost(request,
                              backend.searchVariants,
                              protocol.GASearchVariantsRequest)
    elif request.method == "OPTIONS":
        return "To implement"
    return "Something went wrong"

@app.route('/variantsets/search', methods=['POST', 'OPTIONS'])
def searchVariantSets():
    if request.method == 'POST':
        return handleHTTPPost(request,
                              backend.searchVariantSets,
                              protocol.GASearchVariantSetsRequest)
    elif request.method == "OPTIONS":
        return "To implement"
    return "Something went wrong"

#### CLI
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="GA4GH reference server")
    # Add global options
    parser.add_argument(
        "--port", "-P", default=8000, type=int,
        help="The port to listen on")
    parser.add_argument('--debug', '-d',
                        action='store_true', default=False,
                        help="Turn on the Flask debugger. Not for production.")

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
        backend = args.backend(args.dataDir)
        app.run(host='0.0.0.0', port=args.port, debug=args.debug)