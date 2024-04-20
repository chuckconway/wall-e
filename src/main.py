from fastapi import FastAPI
#from prometheus_fastapi_instrumentator import Instrumentator
from src.endpoints import auth_endpoints, api_endpoints

app = FastAPI()
app.include_router(auth_endpoints.router)
app.include_router(api_endpoints.router)

# Add this block for Prometheus metrics
# instrumentator = Instrumentator().instrument(app)
#
# @app.on_event("startup")
# async def _startup():
#     instrumentator.expose(app)

@app.get("/")
async def home():
    return {"message": "Hello World"}
