from typing import List

from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session

from api import deps, security
from core import settings
from database import crud, mappings, models

router = APIRouter()


@router.post("/recipe", response_model=mappings.StoredRecipeV1, status_code=201)
def create_recipe(
    *,
    payload: mappings.CreateRecipeV1,
    user: mappings.StoredUserV1 = Depends(security.authenticated),
    db: Session = Depends(deps.database)
) -> models.Recipe:
    if crud.recipe.read_name(db, payload.name):
        raise HTTPException(status_code=409)
    # Extract the ingredients from the payload, these will be added later.
    ingredients = payload.ingredients
    payload = payload.dict()
    payload.pop("ingredients")
    # Create the recipe.
    recipe = crud.recipe.create(db, payload, user_id=user.id, commit=False)
    # Now add the ingredients to the recipe.
    for ingredient in ingredients:
        recipe.ingredients.append(models.Ingredient(name=ingredient.name, user_id=user.id))
    db.commit()
    return recipe


@router.get("/recipes", response_model=List[mappings.StoredRecipeV1])
def get_recipes(
    *,
    skip: int = 0,
    limit: int = settings.DATABASE_LIMIT,
    _: mappings.StoredUserV1 = Depends(security.authorised),
    db: Session = Depends(deps.database),
    response: Response
) -> List[models.Recipe]:
    response.headers["Total-Count"] = crud.recipe.count(db)
    return crud.recipe.read_multi(db, skip=skip, limit=limit)


@router.get("/recipes/me", response_model=List[mappings.StoredRecipeV1])
def get_my_recipes(
    *,
    skip: int = 0,
    limit: int = settings.DATABASE_LIMIT,
    published: bool | None = None,
    user: mappings.StoredUserV1 = Depends(security.authenticated),
    db: Session = Depends(deps.database),
    response: Response
) -> List[models.Recipe]:
    response.headers["Total-Count"] = str(crud.recipe.count(db, published=published, user_id=user.id))
    return crud.recipe.read_multi(db, skip=skip, limit=limit, published=published, user_id=user.id)


@router.get("/recipe/random", response_model=mappings.StoredRecipeV1)
def read_random_recipe(
    *,
    db: Session = Depends(deps.database)
) -> models.Recipe:
    if crud.recipe.count(db, published=True) < 3:
        raise HTTPException(status_code=400)
    return crud.recipe.read_random(db, published=True)


@router.get("/recipe/{recipe_id:int}", response_model=mappings.StoredRecipeV1)
def read_recipe(
    *,
    recipe_id: int,
    user: mappings.StoredUserV1 = Depends(security.authenticated),
    db: Session = Depends(deps.database)
) -> models.Recipe:
    recipe: models.Recipe = crud.recipe.read(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404)
    if not (user.admin or user.id == recipe.user_id):
        raise HTTPException(status_code=403)
    return recipe


@router.patch("/recipe/{recipe_id:int}", response_model=mappings.StoredRecipeV1)
def update_recipe(
    *,
    recipe_id: int,
    payload: mappings.UpdateRecipeV1,
    user: mappings.StoredUserV1 = Depends(security.authenticated),
    db: Session = Depends(deps.database)
) -> models.Recipe:
    recipe: models.Recipe = crud.recipe.read(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404)
    if not (user.admin or user.id == recipe.user_id):
        raise HTTPException(status_code=403)
    return crud.recipe.update(db, recipe, payload)


@router.delete("/recipe/{recipe_id:int}", status_code=204)
def delete_recipe(
    *,
    recipe_id: int,
    user: mappings.StoredUserV1 = Depends(security.authenticated),
    db: Session = Depends(deps.database)
) -> None:
    recipe: models.Recipe = crud.recipe.read(db, recipe_id)
    if not recipe:
        raise HTTPException(status_code=404)
    if not (user.admin or user.id == recipe.user_id):
        raise HTTPException(status_code=403)
    crud.recipe.delete(db, recipe_id)
    return None
