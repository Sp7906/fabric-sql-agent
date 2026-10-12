from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from . import agent, db

app = FastAPI(title="Fabric Text-to-SQL Agent")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])


class Question(BaseModel):
    question: str = Field(min_length=3, max_length=500)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/schema")
def schema():
    return db.get_schema()


@app.post("/ask")
def ask(body: Question):
    return agent.ask(body.question)
