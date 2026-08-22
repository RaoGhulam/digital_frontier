from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from app.core.exceptions import AppError
import logging

logger = logging.getLogger("app")


def register_exception_handlers(app: FastAPI):

    @app.exception_handler(AppError)
    async def app_error_handler(request: Request, exc: AppError):
        logger.warning(
            "%s | path=%s | method=%s",
            exc.message,
            request.url.path,
            request.method,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.message
            },
        )

    @app.exception_handler(HTTPException)
    async def http_exception_handler(request: Request, exc: HTTPException):
        logger.warning(
            "%s | path=%s | method=%s",
            exc.detail,
            request.url.path,
            request.method,
        )

        return JSONResponse(
            status_code=exc.status_code,
            content={
                "detail": exc.detail
            },
        )

    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        logger.exception(
            "Unhandled exception | path=%s | method=%s",
            request.url.path,
            request.method,
        )

        return JSONResponse(
            status_code=500,
            content={
                "detail": "Internal server error"
            },
        )