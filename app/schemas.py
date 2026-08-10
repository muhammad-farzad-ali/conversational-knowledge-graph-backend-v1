from pydantic import BaseModel, Field


class UserRequest(BaseModel):
    request: str = Field(..., description="Natural language request from the user")


class SparqlResponse(BaseModel):
    sparql: str = Field(..., description="Generated SPARQL query")
