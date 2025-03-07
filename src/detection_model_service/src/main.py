import uvicorn
from fastapi import FastAPI

from ai_model.router import router as router_model

app = FastAPI()

app.include_router(router_model)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
