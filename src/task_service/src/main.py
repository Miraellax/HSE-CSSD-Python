import asyncio

from contextlib import asynccontextmanager

import uvicorn
from fastapi import FastAPI

from modules.database import engine, init_data
from modules.db_models.models import Base
from modules.tasks.router import router as router_tasks
from modules.ai_models.router import router as router_models
from modules.auth.router import router as router_auth

init_db = True

@asynccontextmanager
async def lifespan(_app: FastAPI):
    if init_db:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await init_data()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(router_tasks)

app.include_router(router_models)

app.include_router(router_auth)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)


# RUN
# fastapi run src/app/main.py