from fastapi import FastAPI

from app.schemas import ResultsResponse, SparqlRequest, SparqlResponse, UserRequest

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

TABLE_MARKDOWN = """\
|  # | ?pubTitle                                            | ?Authors | ?Venues | ?Years |
| -: | ---------------------------------------------------- | -------: | ------: | -----: |
|  1 | ≪-separating domains, strong-compact spaces an[...]  |        1 |       1 |      1 |
|  2 | Model identification control strategy for coupl[...] |        4 |       1 |      1 |
|  3 | host device - Generic programming in Cud[...]        |        1 |       1 |      1 |
|  4 | derivations: improvisation for tenor saxophone [...] |        1 |       1 |      1 |
|  5 | Generalized Fuzzy Ideals of BCH-Algebra.             |        2 |       1 |      1 |
|  6 | knowscape - a collective knowledge architecture[...] |        2 |       1 |      1 |
|  7 | knowscape mobile at DIS2004, Cambridge.              |        4 |       1 |      1 |
|  8 | knowscape mobile, associating territory of data[...] |        4 |       1 |      1 |
|  9 | knowscape, a 3D multi-user experimental web bro[...] |        4 |       1 |      1 |\
"""


@app.post("/sparql", response_model=SparqlResponse)
def generate_sparql(user_request: UserRequest) -> SparqlResponse:
    return SparqlResponse(sparql=SPARQL_QUERY)


@app.post("/results", response_model=ResultsResponse)
def get_results(sparql_request: SparqlRequest) -> ResultsResponse:
    return ResultsResponse(table=TABLE_MARKDOWN)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
