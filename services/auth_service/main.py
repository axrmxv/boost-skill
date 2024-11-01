from fastapi import FastAPI
from services.auth_service.api.routes import auth_router


app = FastAPI()

app.include_router(auth_router, prefix="/auth", tags=["auth"])


@app.get("/")
async def root():
    return {"message": "AuthService is running"}
