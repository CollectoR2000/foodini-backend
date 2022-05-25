import time

from fastapi import FastAPI, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles

from api import docs, health, v1
from core import settings


def description() -> str:
    with open(settings.PROJECT_CHANGELOG, "r") as changelog:
        changes = changelog.read()
        changes = changes.replace("# Changelog", "## Changelog")
        changes = changes.replace("## [", "### [")
        return settings.PROJECT_DESCRIPTION + "\n" + changes


app = FastAPI(
    title=settings.PROJECT_TITLE,
    description=description(),
    version=settings.PROJECT_VERSION,
    openapi_url=settings.DOCS_OPENAPI,
    docs_url=None if settings.DOCS_OFFLINE else settings.DOCS_SWAGGER,
    redoc_url=None if settings.DOCS_OFFLINE else settings.DOCS_REDOC
)

# Add the CORS middleware.
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=settings.CORS_ORIGIN_REGEX,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=settings.CORS_ORIGINS_EXPOSE_HEADERS
)

# Mount the static directory.
app.mount(settings.API_STATIC_PREFIX, StaticFiles(directory=settings.API_STATIC_DIRECTORY), name="static")

# Include the docs router containing the Swagger and Redoc endpoints.
app.include_router(docs.router, tags=["Docs"])

# Add the healthcheck router.
app.include_router(health.router, prefix=settings.API_HEALTH_PREFIX, tags=["Health"])

# Include the API endpoint routers.
app.include_router(v1.router, prefix=f"{settings.API_ENDPOINT_PREFIX}{settings.API_V1_PREFIX}")


# Add middleware to add processing time as header.
@app.middleware("http")
async def add_process_time_header(request: Request, call_next: callable) -> Response:
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["Process-Time"] = str(process_time)
    return response


# Default redirect from root to docs.
@app.get("/", include_in_schema=False)
async def swagger_redirect() -> RedirectResponse:
    return RedirectResponse(url="/docs")
