from fastapi import FastAPI
from src.endpoints import auth_endpoints

app = FastAPI()
app.include_router(auth_endpoints.router)


@app.get("/")
async def home():
    return {"message": "Hello World"}
