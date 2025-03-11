from flask import Flask, request, jsonify
from SPARQLWrapper import SPARQLWrapper, JSON

app = Flask(__name__)

# GraphDB SPARQL Endpoint (Make sure this URL is correct for your GraphDB setup)
SPARQL_ENDPOINT = "http://localhost:7200/repositories/ecology_ontology"

sparql = SPARQLWrapper(SPARQL_ENDPOINT)

@app.route('/search', methods=['GET'])
def search():
    query_type = request.args.get('type', 'affects')
    query_param = request.args.get('query')

    if query_type == 'affects':
        sparql.setQuery(f"""
        PREFIX eco: <http://example.org/eco#>
        SELECT ?result WHERE {{
            ?result eco:affects eco:{query_param} .
        }}
        """)

    elif query_type == 'biotic':
        sparql.setQuery("""
        PREFIX eco: <http://example.org/eco#>
        SELECT ?bioticFactor WHERE {
            ?bioticFactor rdf:type eco:BioticFactor .
        }
        """)

    elif query_type == 'abiotic':
        sparql.setQuery("""
        PREFIX eco: <http://example.org/eco#>
        SELECT ?abioticFactor WHERE {
            ?abioticFactor rdf:type eco:AbioticFactor .
        }
        """)

    elif query_type == 'relationship':
        sparql.setQuery(f"""
        PREFIX eco: <http://example.org/eco#>
        SELECT ?relation ?entity WHERE {{
            eco:{query_param} ?relation ?entity .
        }}
        """)

    else:
        return jsonify({"error": "Invalid query type"}), 400

    try:
        sparql.setReturnFormat(JSON)
        results = sparql.query().convert()
        return jsonify(results["results"]["bindings"])
    except Exception as e:
        return jsonify({"error": f"SPARQL Query Failed: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5060)
