from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import admin, comment, post, reaction, user
from app.core.exception_handlers import register_exception_handlers
from app.core.logging_config import setup_logging


# Setup application logging
setup_logging()


# Create FastAPI app
app = FastAPI(title="My App")


# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Next.js frontend
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Register global exception handlers
register_exception_handlers(app)


# API Routes
app.include_router(user.router, prefix="/api")
app.include_router(post.router, prefix="/api")
app.include_router(comment.router, prefix="/api")
app.include_router(reaction.router, prefix="/api")
app.include_router(admin.router, prefix="/api")


@app.get("/")
def root():
    return {"status": "ok"}