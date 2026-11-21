import os

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
from celery.result import AsyncResult
from sqlalchemy import create_engine, text
import strawberry
from strawberry.fastapi import GraphQLRouter

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg://postgres:secret@db:5432/appdb",
)
db_engine = create_engine(DATABASE_URL, pool_pre_ping=True)

app = FastAPI(title="KT5 — Продвинутые темы backend-разработки", version="1.0.0")


class WelcomeRequest(BaseModel):
    email: EmailStr
    username: str


@app.get("/")
def home():
    return {
        "message": "KT5 API is running",
        "docs": "/docs",
        "graphql": "/graphql",
    }


@app.get("/db-health")
def database_health():
    try:
        with db_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception as exc:
        raise HTTPException(status_code=503, detail="Database unavailable") from exc


@app.post("/tasks/welcome", status_code=202)
def create_welcome_task(data: WelcomeRequest):
    from tasks import send_welcome_email
    task = send_welcome_email.delay(data.email, data.username)
    return {
        "task_id": task.id,
        "status": "queued",
        "message": "Background task accepted",
    }


@app.get("/tasks/{task_id}")
def get_task_status(task_id: str):
    from tasks import celery_app
    result = AsyncResult(task_id, app=celery_app)
    response = {"task_id": task_id, "status": result.status}
    if result.successful():
        response["result"] = result.result
    elif result.failed():
        response["error"] = str(result.result)
    return response


@strawberry.type
class Query:
    @strawberry.field
    def hello(self, name: str = "Backend") -> str:
        return f"Hello, {name}! This is a GraphQL example."

    @strawberry.field
    def course_topic(self) -> str:
        return "Advanced backend development: background tasks and alternative APIs"


schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")
