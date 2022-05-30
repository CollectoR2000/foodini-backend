from fastapi import APIRouter

from .endpoints import authentication, recipe, user

router = APIRouter()
router.include_router(authentication.router, tags=["Authentication"])
router.include_router(recipe.router, tags=["Recipe"])
router.include_router(user.router, tags=["User"])
