import base64
import json

from fastapi import  Request
from fastapi.templating import Jinja2Templates

from typing import Annotated

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .. import database
from ..auth.router import get_current_user
from ..auth.schema import User
from ..tasks.router import get_task_result_by_id
from ..ai_models import dao as ai_models_dao

router = APIRouter(prefix='/ui')
templates = Jinja2Templates(directory='modules/templates')


# Pae to visualize results
@router.get('/results/{task_id}')
async def get_task_results(task_id: int,
                           request: Request,
                           current_user: Annotated[User, Depends(get_current_user)],
                           db: AsyncSession = Depends(database.get_db)
                           ):
    res = await get_task_result_by_id(current_user=current_user, task_id=task_id, db=db)
    res_json = json.loads(res.body)

    for primitive in res_json["result"]["primitives"]:
        if primitive["primitive_class"] == "sphere":
            primitive["primitive_class"] = "сфера"
        elif primitive["primitive_class"] == "cube":
            primitive["primitive_class"] = "куб"
        elif primitive["primitive_class"] == "torus":
            primitive["primitive_class"] = "торус"
        elif primitive["primitive_class"] == "cylinder":
            primitive["primitive_class"] = "цилиндр"
        elif primitive["primitive_class"] == "cone":
            primitive["primitive_class"] = "конус"

    return templates.TemplateResponse(name='results.html', context={'request': request, 'res': res_json})

# Page to send image for prediction
@router.get('/tasks')
async def get_task_results(request: Request,
                           current_user: Annotated[User, Depends(get_current_user)],
                           db: AsyncSession = Depends(database.get_db)
                           ):
    d_models = [(model.id, model.name, "detection_model") for model in await ai_models_dao.get_detection_models(db=db)]
    c_models = [(model.id, model.name, "classification_model") for model in
                await ai_models_dao.get_classification_models(db=db)]


    return templates.TemplateResponse(name='input.html', context={'request': request,
                                                                  'token':request.headers["authorization"],
                                                                  'd_models': d_models,
                                                                  'c_models': c_models})
