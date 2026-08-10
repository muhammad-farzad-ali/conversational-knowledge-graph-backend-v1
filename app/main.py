from fastapi import FastAPI

from app.schemas import SparqlResponse, UserRequest

app = FastAPI(title="Conversational Knowledge Graph Backend")

SPARQL_QUERY = """\
PREFIX dblp: <https://dblp.org/rdf/schema#>

SELECT
  ?pubTitle
  (COUNT(DISTINCT ?authorName) AS ?Authors)
  (COUNT(DISTINCT ?venue) AS ?Venues)
  (COUNT(DISTINCT ?year) AS ?Years)
WHERE {
  ?pub a dblp:Publication .
  ?pub dblp:title ?pubTitle .

  OPTIONAL {
    ?pub dblp:authoredBy ?author .
    ?author dblp:primaryCreatorName ?authorName .
  }

  OPTIONAL {
    ?pub dblp:publishedIn ?venue .
  }

  OPTIONAL {
    ?pub dblp:yearOfPublication ?year .
  }
}
GROUP BY ?pubTitle
ORDER BY ASC(?pubTitle)\
"""


@app.post("/sparql", response_model=SparqlResponse)
def generate_sparql(user_request: UserRequest) -> SparqlResponse:
    return SparqlResponse(sparql=SPARQL_QUERY)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
