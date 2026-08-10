# API Reference

**Base URL:** `http://127.0.0.1:8000`

---

## Endpoints

### `GET /health`

Health check endpoint.

**Response** `200 OK`:

```json
{
  "status": "ok"
}
```

---

### `POST /sparql`

Returns a SPARQL query for DBLP publications.

**Request** `POST /sparql`:

```json
{
  "request": "List publications with authors, venues, and years"
}
```

| Field     | Type   | Required | Description                          |
| --------- | ------ | -------- | ------------------------------------ |
| `request` | string | Yes      | Natural language request from user   |

**Response** `200 OK`:

```json
{
  "sparql": "PREFIX dblp: <https://dblp.org/rdf/schema#>\n\nSELECT\n  ?pubTitle\n  (COUNT(DISTINCT ?authorName) AS ?Authors)\n  (COUNT(DISTINCT ?venue) AS ?Venues)\n  (COUNT(DISTINCT ?year) AS ?Years)\nWHERE {\n  ?pub a dblp:Publication .\n  ?pub dblp:title ?pubTitle .\n  OPTIONAL {\n    ?pub dblp:authoredBy ?author .\n    ?author dblp:primaryCreatorName ?authorName .\n  }\n  OPTIONAL {\n    ?pub dblp:publishedIn ?venue .\n  }\n  OPTIONAL {\n    ?pub dblp:yearOfPublication ?year .\n  }\n}\nGROUP BY ?pubTitle\nORDER BY ASC(?pubTitle)"
}
```

| Field    | Type   | Description              |
| -------- | ------ | ------------------------ |
| `sparql` | string | Generated SPARQL query   |

**cURL:**

```bash
curl -X POST http://127.0.0.1:8000/sparql \
  -H "Content-Type: application/json" \
  -d '{"request": "List publications with authors, venues, and years"}'
```

---

### `POST /results`

Returns query results as a markdown table. Accepts any SPARQL query and returns a hardcoded result table.

**Request** `POST /results`:

```json
{
  "sparql": "PREFIX dblp: <https://dblp.org/rdf/schema#> SELECT ?pubTitle WHERE { ?pub dblp:title ?pubTitle }"
}
```

| Field    | Type   | Required | Description           |
| -------- | ------ | -------- | --------------------- |
| `sparql` | string | Yes      | SPARQL query to send  |

**Response** `200 OK`:

```json
{
  "table": "|  # | ?pubTitle                                            | ?Authors | ?Venues | ?Years |\n| -: | ---------------------------------------------------- | -------: | ------: | -----: |\n|  1 | ≪-separating domains, strong-compact spaces an[...]  |        1 |       1 |      1 |\n|  2 | Model identification control strategy for coupl[...] |        4 |       1 |      1 |\n|  3 | host device - Generic programming in Cud[...]        |        1 |       1 |      1 |\n|  4 | derivations: improvisation for tenor saxophone [...] |        1 |       1 |      1 |\n|  5 | Generalized Fuzzy Ideals of BCH-Algebra.             |        2 |       1 |      1 |\n|  6 | knowscape - a collective knowledge architecture[...] |        2 |       1 |      1 |\n|  7 | knowscape mobile at DIS2004, Cambridge.              |        4 |       1 |      1 |\n|  8 | knowscape mobile, associating territory of data[...] |        4 |       1 |      1 |\n|  9 | knowscape, a 3D multi-user experimental web bro[...] |        4 |       1 |      1 |"
}
```

| Field   | Type   | Description                         |
| ------- | ------ | ----------------------------------- |
| `table` | string | Markdown table of query results     |

**cURL:**

```bash
curl -X POST http://127.0.0.1:8000/results \
  -H "Content-Type: application/json" \
  -d '{"sparql": "PREFIX dblp: <https://dblp.org/rdf/schema#> SELECT ?pubTitle WHERE { ?pub dblp:title ?pubTitle }"}'
```

---

## Error Responses

### `422 Validation Error`

Returned when request body fails validation.

```json
{
  "detail": [
    {
      "type": "missing",
      "loc": ["body", "request"],
      "msg": "Field required",
      "input": {},
      "url": "https://errors.pydantic.dev/2.11/missing"
    }
  ]
}
```

---

## UI Implementation Notes

1. **Input:** Provide a text input for the user to type a natural language request or SPARQL query.
2. **Flow:**
   - User enters a request → call `POST /sparql` → display the returned SPARQL.
   - User submits SPARQL → call `POST /results` → parse and render the markdown table.
3. **Table rendering:** The `table` field contains standard markdown. Use a markdown renderer or parse the pipe-delimited format into an HTML `<table>`.
4. **Error handling:** Show validation errors from the `detail` array when the backend returns 422.
