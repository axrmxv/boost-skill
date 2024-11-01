import uvicorn

from fastapi import FastAPI
from fastapi.routing import APIRouter

from api.hendlers import user_router


# API Routers
app = FastAPI(title="Boost Skill")

main_api_router = APIRouter()

main_api_router.include_router(user_router, prefix="/user", tags=["user"])
app.include_router(main_api_router)


if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8027)
