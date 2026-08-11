from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.agents import router, sparql_generator, table_formatter
from app.schemas import ChatRequest, ChatResponse

app = FastAPI(title="Conversational Knowledge Graph Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    if router.is_sparql(request.message):
        result = table_formatter.execute(request.message)
        return ChatResponse(type="table", content=result)
    else:
        result = sparql_generator.execute(request.message)
        return ChatResponse(type="sparql", content=result)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
