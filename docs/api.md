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

### `POST /chat`

Single endpoint that handles both natural language requests and SPARQL queries. The system automatically detects the input type and routes to the appropriate agent.

**Request** `POST /chat`:

```json
{
  "message": "List publications with authors, venues, and years"
}
```

| Field     | Type   | Required | Description                                    |
| --------- | ------ | -------- | ---------------------------------------------- |
| `message` | string | Yes      | User message (natural language or SPARQL query) |

**Response — Natural Language Input** `200 OK`:

When the input is natural language, the system generates a SPARQL query:

```json
{
  "type": "sparql",
  "content": "PREFIX dblp: <https://dblp.org/rdf/schema#>\n\nSELECT\n  ?pubTitle\n  (COUNT(DISTINCT ?authorName) AS ?Authors)\n  (COUNT(DISTINCT ?venue) AS ?Venues)\n  (COUNT(DISTINCT ?year) AS ?Years)\nWHERE {\n  ?pub a dblp:Publication .\n  ?pub dblp:title ?pubTitle .\n  OPTIONAL {\n    ?pub dblp:authoredBy ?author .\n    ?author dblp:primaryCreatorName ?authorName .\n  }\n  OPTIONAL {\n    ?pub dblp:publishedIn ?venue .\n  }\n  OPTIONAL {\n    ?pub dblp:yearOfPublication ?year .\n  }\n}\nGROUP BY ?pubTitle\nORDER BY ASC(?pubTitle)"
}
```

**Response — SPARQL Input** `200 OK`:

When the input is a SPARQL query, the system returns results as a markdown table:

```json
{
  "type": "table",
  "content": "|  # | ?pubTitle                                            | ?Authors | ?Venues | ?Years |\n| -: | ---------------------------------------------------- | -------: | ------: | -----: |\n|  1 | ≪-separating domains, strong-compact spaces an[...]  |        1 |       1 |      1 |\n|  2 | Model identification control strategy for coupl[...] |        4 |       1 |      1 |\n|  3 | host device - Generic programming in Cud[...]        |        1 |       1 |      1 |\n|  4 | derivations: improvisation for tenor saxophone [...] |        1 |       1 |      1 |\n|  5 | Generalized Fuzzy Ideals of BCH-Algebra.             |        2 |       1 |      1 |\n|  6 | knowscape - a collective knowledge architecture[...] |        2 |       1 |      1 |\n|  7 | knowscape mobile at DIS2004, Cambridge.              |        4 |       1 |      1 |\n|  8 | knowscape mobile, associating territory of data[...] |        4 |       1 |      1 |\n|  9 | knowscape, a 3D multi-user experimental web bro[...] |        4 |       1 |      1 |"
}
```

| Field     | Type   | Description                                |
| --------- | ------ | ------------------------------------------ |
| `type`    | string | `"sparql"` or `"table"`                    |
| `content` | string | SPARQL query string or markdown table      |

**cURL — Natural Language:**

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "List publications with authors, venues, and years"}'
```

**cURL — SPARQL:**

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "PREFIX dblp: <https://dblp.org/rdf/schema#> SELECT ?pubTitle WHERE { ?pub dblp:title ?pubTitle }"}'
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
      "loc": ["body", "message"],
      "msg": "Field required",
      "input": {},
      "url": "https://errors.pydantic.dev/2.11/missing"
    }
  ]
}
```

---

## Architecture

```
User → POST /chat → router.is_sparql(message)
                     ├─ Yes → table_formatter.execute(sparql) → {type: "table", content: "..."}
                     └─ No  → sparql_generator.execute(nl)    → {type: "sparql", content: "..."}
```

| Agent              | Module                          | Responsibility                     |
| ------------------ | ------------------------------- | ---------------------------------- |
| Router             | `app/agents/router.py`          | Detects if input is SPARQL or NL   |
| SPARQL Generator   | `app/agents/sparql_generator.py`| Generates SPARQL from NL request   |
| Table Formatter    | `app/agents/table_formatter.py` | Formats SPARQL results as table    |

---

## UI Implementation Notes

1. **Single input:** Provide one text input for the user to type either natural language or SPARQL.
2. **Response handling:** Check the `type` field in the response:
   - `"sparql"` → display the SPARQL query in a code block.
   - `"table"` → parse and render the markdown table.
3. **Table rendering:** The `content` field contains standard markdown. Use a markdown renderer or parse the pipe-delimited format into an HTML `<table>`.
4. **Error handling:** Show validation errors from the `detail` array when the backend returns 422.
