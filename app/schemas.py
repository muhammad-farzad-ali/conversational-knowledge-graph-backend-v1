from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    request: str = Field(..., description="Natural language request from the user")


class SparqlResponse(BaseModel):
    sparql: str = Field(..., description="Generated SPARQL query")


class SparqlRequest(BaseModel):
    sparql: str = Field(..., description="SPARQL query to execute")


class ResultsResponse(BaseModel):
    table: str = Field(..., description="Markdown table of query results")
