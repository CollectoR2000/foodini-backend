from fastapi import APIRouter
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html, get_swagger_ui_oauth2_redirect_html
from fastapi.responses import HTMLResponse

from core import settings

router = APIRouter()


@router.get(settings.DOCS_SWAGGER, include_in_schema=False)
async def swagger() -> HTMLResponse:
    return get_swagger_ui_html(
        openapi_url=settings.DOCS_OPENAPI,
        title=settings.PROJECT_TITLE + " - Swagger UI",
        swagger_js_url=f"{settings.API_STATIC_PREFIX}/swagger-ui-bundle.js",
        swagger_css_url=f"{settings.API_STATIC_PREFIX}/swagger-ui.css",
        swagger_favicon_url=f"{settings.API_STATIC_PREFIX}/swagger.favicon.png"
    )


@router.get(settings.DOCS_SWAGGER_OAUTH, include_in_schema=False)
async def swagger_oauth() -> HTMLResponse:
    return get_swagger_ui_oauth2_redirect_html()


@router.get(settings.DOCS_REDOC, include_in_schema=False)
async def redoc() -> HTMLResponse:
    return get_redoc_html(
        openapi_url=settings.DOCS_OPENAPI,
        title=settings.PROJECT_TITLE + " - ReDoc",
        redoc_js_url=f"{settings.API_STATIC_PREFIX}/redoc.standalone.js",
        redoc_favicon_url=f"{settings.API_STATIC_PREFIX}/redoc.favicon.png",
        with_google_fonts=None
    )
