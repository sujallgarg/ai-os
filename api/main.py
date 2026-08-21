"""
AI Agent Platform API.
"""

from fastapi import (
    FastAPI
)

from fastapi.middleware.cors import (
    CORSMiddleware
)

from api.routes import (
    goals,
    jobs,
    approvals,
    agents,
    tasks
)

from api.routes.events import (
    router as events_router
)


app = FastAPI(
    title="AI Agent Platform",
    description="Autonomous multi-agent AI system.",
    version="1.0.0"
)


# ================================================================
# CORS
# ================================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:3001",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# ================================================================
# ROUTES
# ================================================================

app.include_router(
    goals.router
)

app.include_router(
    jobs.router
)

app.include_router(
    approvals.router
)

app.include_router(
    agents.router
)

app.include_router(
    tasks.router
)

app.include_router(
    events_router
)


# ================================================================
# HEALTH & ROOT
# ================================================================

@app.get("/")
def root():
    return {
        "name": "AI Agent Platform",
        "status": "online",
        "version": "1.0.0"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "ai-agent-platform"
    }