from typing import Annotated, Union

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from .. import database
from . import schema as models_schemas
from . import dao as models_dao
from ..auth.router import get_current_user
from ..auth.schema import User

router = APIRouter(prefix="/models")


# 7) GET api/models
@router.get("/", response_model=None)
def get_model_list(current_user: Annotated[User, Depends(get_current_user)],
                   db: Session = Depends(database.get_db)
                   ) -> JSONResponse:

    # will get models only if auth
    classification_models = models_dao.get_classification_models(db=db)
    detection_models = models_dao.get_detection_models(db=db)

    result = {
        "detection_models": [
            {
                "model_name": model.name,
                "model_id": model.id
            } for model in detection_models
        ],
        "classification_models": [
            {
                "model_name": model.name,
                "model_id": model.id
            } for model in classification_models
        ]
    }
    return JSONResponse(content=result)

# await (await fetch('/models', {headers:{'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJmaXJzdCIsImV4cCI6MTc0MDA2MzI5Nn0.9XloWont-KzCBYGDYDGz5N1tQv2LD8kDusZg684fApc'}})).json()
