import asyncio

import aiofiles
import aiohttp
from pathlib import Path
from typing import Union, Annotated

from fastapi import APIRouter, Depends, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from .. import database
from . import schema as task_schemas
from . import dao as task_dao
from ..predictions import dao as predictions_dao
from ..ai_models import dao as ai_models_dao
from ..status import dao as status_dao
from ..scene_class import dao as scene_class_dao
from ..primitive_class import dao as primitive_class_dao
from ..auth.router import get_current_user
from ..auth.schema import User

router = APIRouter(prefix="/tasks")

INPUT_IMAGE_SAVE_PATH = "./images/"

# GET api/tasks/{id:integer}
@router.get("/{task_id}", response_model=task_schemas.Task)
async def get_task_by_id(current_user: Annotated[User, Depends(get_current_user)],
                   task_id: int,
                   db: AsyncSession = Depends(database.get_db)
                   ) -> Union[task_schemas.Task, None]:
    # will get task only if auth
    task = await task_dao.get_task(db=db, owner_id=current_user.id, task_id=task_id)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} does not exist.")
    return task

# await (await fetch('/tasks/1', {headers:{'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmaXJzdCIsImV4cCI6MTc0MDA2MzI5Nn0.9XloWont-KzCBYGDYDGz5N1tQv2LD8kDusZg684fApc'}})).json()


# 2) POST api/tasks
@router.post("/", response_model=None)
async def post_task(
                    current_user: Annotated[User, Depends(get_current_user)],
                    image_file: UploadFile,
                    detection_model_id: int,
                    classification_model_id: int,
                    db: AsyncSession = Depends(database.get_db)) -> JSONResponse:

    # will post only if auth
    if image_file is not None:
        d_models = [(model.id, model.name, "detection_model") for model in await ai_models_dao.get_detection_models(db=db)]
        c_models = [(model.id, model.name, "classification_model") for model in await ai_models_dao.get_classification_models(db=db)]

        d_model_ids = [model[0] for model in d_models]
        c_model_ids = [model[0] for model in c_models]

        if detection_model_id not in d_model_ids or classification_model_id not in c_model_ids:
            raise HTTPException(status_code=400,
                                detail=f"Model id was not correct. Choose from (id, name, type) {d_models+c_models}.")

        input_path = image_file.filename
        async with aiofiles.open(input_path, 'wb') as out_file:
            while content := await image_file.read(1024):  # async read chunk
                await out_file.write(content)  # async write chunk

        # get "queued" status id
        statuses = await status_dao.get_status_values(db=db)
        task = await task_dao.create_task(
            db=db,
            task=task_schemas.TaskCreate(
                owner_id=current_user.id,
                detection_model_id=detection_model_id,
                classification_model_id=classification_model_id,
                status_id=next((status.id for status in statuses if status.status == "queued"), None),
                input_path=input_path)
        )

        if task is not None:
            result = { "id": task.id }

            return JSONResponse(content=result)


# 3) GET api/tasks
@router.get("/", response_model=None)
async def get_current_user_tasks(current_user: Annotated[User, Depends(get_current_user)],
                           db: AsyncSession = Depends(database.get_db)
                           ) -> JSONResponse:

    # will get tasks only if auth
    tasks = await task_dao.get_tasks_by_owner(db=db, owner_id=current_user.id)
    statuses = await status_dao.get_status_values(db=db)

    result = {"tasks": [{"id": task.id,
                       "status": next((status.status for status in statuses if status.id == task.status_id), None),
                       "created_at": task.created_at.isoformat(),
                       "input_path": task.input_path
                       } for task in tasks]
    }

    return JSONResponse(content=result)

# await (await fetch('/tasks', {headers:{'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmaXJzdCIsImV4cCI6MTc0MDA2MzI5Nn0.9XloWont-KzCBYGDYDGz5N1tQv2LD8kDusZg684fApc'}})).json()


# 4) GET api/tasks/{id:integer}/status
@router.get("/{task_id}/status", response_model=None)
async def get_task_status_by_id(current_user: Annotated[User, Depends(get_current_user)],
                         task_id: int,
                         db: AsyncSession = Depends(database.get_db)
                         ) -> JSONResponse:

    # will get task only if auth
    task = await task_dao.get_task(db=db, owner_id=current_user.id, task_id=task_id)
    statuses = await status_dao.get_status_values(db=db)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} does not exist.")
    else:
        result = {
            "id": task.id,
            "status": next((status.status for status in statuses if status.id == task.status_id), None),
        }
        return JSONResponse(content=result)

# await (await fetch('/tasks/1/status', {headers:{'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmaXJzdCIsImV4cCI6MTc0MDA2MzI5Nn0.9XloWont-KzCBYGDYDGz5N1tQv2LD8kDusZg684fApc'}})).json()


# 5) GET api/tasks/{id:integer}/input
# actually response_model=FileResponse, but there is a bug, that doesn't allow it to be used
@router.get("/{task_id}/input", response_model=None)
async def get_task_input_by_id(current_user: Annotated[User, Depends(get_current_user)],
                         task_id: int,
                         db: AsyncSession = Depends(database.get_db)
                         ) -> FileResponse:

    # will get task only if auth
    task = await task_dao.get_task(db=db, owner_id=current_user.id, task_id=task_id)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} does not exist.")
    else:
        task_path = Path(INPUT_IMAGE_SAVE_PATH + task.input_path)
        if not task_path.is_file():
            raise HTTPException(status_code=404, detail=f"Input image file for task with id {task_id} does not exist in image directory.")

        return FileResponse(task_path)

# await (await fetch('/tasks/1/input', {headers:{'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmaXJzdCIsImV4cCI6MTc0MDA2MzI5Nn0.9XloWont-KzCBYGDYDGz5N1tQv2LD8kDusZg684fApc'}})).url


# 6) GET api/tasks/{id:integer}/result
@router.get("/{task_id}/result", response_model=None)
async def get_task_result_by_id(current_user: Annotated[User, Depends(get_current_user)],
                         task_id: int,
                         db: AsyncSession = Depends(database.get_db)
                         ) -> JSONResponse:

    # will get task only if auth
    task = await task_dao.get_task(db=db, owner_id=current_user.id, task_id=task_id)

    if task is None:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} does not exist.")
    else:
        # will get predictions only if auth and owner of task
        statuses = await status_dao.get_status_values(db=db)
        scene_classes = await scene_class_dao.get_scene_class_values(db=db)
        primitive_classes = await primitive_class_dao.get_primitive_class_values(db=db)

        preds = await predictions_dao.get_predictions(db=db, task_id=task_id)

        result = {
            "id": task.id,
            "status": next((status.status for status in statuses if status.id == task.status_id), None),
            "result": {
                "image_class": next((scene_class.scene_class for scene_class in scene_classes if scene_class.id == task.scene_class_id), None),
                "primitives": [
                    {
                        "primitive_class": next((primitive_class.primitive_class for primitive_class in primitive_classes if primitive_class.id == pred.primitive_class_id), None),
                        "x": pred.x_coord,
                        "y": pred.y_coord,
                        "width": pred.width,
                        "height": pred.height,
                        "rotation": pred.rotation,
                        "probability": pred.probability
                    } for pred in preds
                ]
            }
        }
        return JSONResponse(content=result)

# await (await fetch('/tasks/1/result', {headers:{'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmaXJzdCIsImV4cCI6MTc0MDA2MzI5Nn0.9XloWont-KzCBYGDYDGz5N1tQv2LD8kDusZg684fApc'}})).json()


# 8) DELETE api/tasks/{id:integer}/result
@router.delete("/{task_id}", response_model=None)
async def delete_task_by_id(current_user: Annotated[User, Depends(get_current_user)],
                      task_id: int,
                      db: AsyncSession = Depends(database.get_db)
                      ) -> JSONResponse:

    # will delete task only if auth
    task = await task_dao.get_task(db=db, owner_id=current_user.id, task_id=task_id)

    if task is not None:
        deleted_task_id = await task_dao.delete_task(db=db, task=task)

        result = {
            "id": deleted_task_id
        }
        return JSONResponse(content=result)
    else:
        raise HTTPException(status_code=404, detail=f"Task with id {task_id} does not exist.")

# await (await fetch('/tasks/1', {method: "DELETE", headers:{'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmaXJzdCIsImV4cCI6MTc0MDA2MzI5Nn0.9XloWont-KzCBYGDYDGz5N1tQv2LD8kDusZg684fApc'}})).json()


# Тестовый POST метод для взаимодействия с контейнером модели
@router.post("/test_service_connection", response_model=None)
async def test_service_connection(
                    current_user: Annotated[User, Depends(get_current_user)],
                    image_file: UploadFile,
                    detection_model_id: int,
                    db: AsyncSession = Depends(database.get_db)) -> JSONResponse:

    # will try post task only if auth
    async with aiohttp.ClientSession() as session:
            data = aiohttp.FormData()
            data.add_field("image_file", image_file.file, filename=image_file.filename, content_type=image_file.content_type)
            async with session.post("http://detection_model_1/model/", data=data) as response:
                return JSONResponse(content=await response.json())
