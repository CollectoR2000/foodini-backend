from fastapi import APIRouter

from .endpoints import authentication, recipe

router = APIRouter()
router.include_router(authentication.router, tags=["Authentication"])
router.include_router(recipe.router, tags=["Recipe"])
