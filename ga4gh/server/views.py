from . import app
from flask import Response, request, render_template
import ga4gh.protocol as protocol
from ga4gh.backends import WormtableBackend, TabixBackend


# Helper function
# TODO: Does this need http://flask-cors.readthedocs.org/en/latest/
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


@app.route('/')
def index():
    """ Returns website for a beacon interface
    """
    # TODO: Programmatically fetch variaint_sets
    # variant_sets = [x for x in os.listdir(args.dataDir) if isdir(join(args.dataDir, x))]
    if app.config["BEACON"]:
        return render_template('beacon.haml', variant_sets=["1kg_phase3"])
    else:
        return render_template('index.haml')


if app.config["BEACON"]:
    @app.route('/search', methods=["POST"])
    def search():
        """
        Searches beacon
        """
        query = protocol.GASearchVariantsRequest()
        query.variantSetIds = [request.values["population"]]
        query.referenceName = request.values["chr"]
        query.start = int(request.values['coord'])
        query.end = int(request.values['coord'])

        result = app.config["VariantBackend"].searchVariants(query)
        for var in result.variants:
            if request.values["allele"] == "D":
                if len(var.referenceBases) > 1:
                    return "True"
            else:
                for alt in var.alternateBases:
                    if request.values["allele"] in alt:
                        return "True"
        return "False"


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
                          app.config["VariantBackend"].searchVariantSets,
                          protocol.GASearchVariantSetsRequest)


@app.route('/variants/search', methods=['POST'])
def searchVariants():
    return handleHTTPPost(request,
                          app.config["VariantBackend"].searchVariants,
                          protocol.GASearchVariantsRequest)
