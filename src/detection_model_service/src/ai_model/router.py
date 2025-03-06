from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

from .ai_model import process


router = APIRouter(prefix="/model")


# POST api/model
@router.post("/", response_model=None)
async def post_task(image_file: UploadFile) -> JSONResponse:

    if image_file is not None:
        predictions = await process(image_file)

        if predictions is not None:
            return JSONResponse(content=predictions)
