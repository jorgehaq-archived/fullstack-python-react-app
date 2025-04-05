from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter
from typing import List, Optional

from app.core.config import settings

# Ejemplo básico de schema GraphQL
@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, world!"

    @strawberry.field
    def echo(self, message: str) -> str:
        return f"Echo: {message}"

# Crear schema GraphQL
schema = strawberry.Schema(query=Query)

# Crear router GraphQL
graphql_app = GraphQLRouter(schema)

# Crear aplicación FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description=settings.DESCRIPTION,
    openapi_url=f"{settings.API_PREFIX}/openapi.json",
    docs_url="/docs",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir router GraphQL
app.include_router(graphql_app, prefix="/graphql")

# Endpoint de estado
@app.get("/health")
def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)