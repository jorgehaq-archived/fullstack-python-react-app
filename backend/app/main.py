from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional

from app.core.config import settings

# Ejemplo básico de schema GraphQL
@strawberry.type
class User:
    id: str
    name: str
    email: str

@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, Clean Architecture World!"

    @strawberry.field
    def users(self) -> List[User]:
        # Mock data
        return [
            User(id="1", name="John Doe", email="john@example.com"),
            User(id="2", name="Jane Smith", email="jane@example.com"),
        ]

schema = strawberry.Schema(query=Query)
graphql_app = GraphQLRouter(schema)

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(graphql_app, prefix="/graphql")

@app.get("/")
def root():
    return {"message": "Welcome to Clean Architecture API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)