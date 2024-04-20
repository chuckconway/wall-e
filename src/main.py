from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
#from prometheus_fastapi_instrumentator import Instrumentator
from src.endpoints import auth_endpoints, api_endpoints

app = FastAPI()
app.include_router(auth_endpoints.router)
app.include_router(api_endpoints.router)

templates = Jinja2Templates(directory="src/client")
app.mount("/static", StaticFiles(directory="src/client/static"), name="static")


# Add this block for Prometheus metrics
# instrumentator = Instrumentator().instrument(app)
#
# @app.on_event("startup")
# async def _startup():
#     instrumentator.expose(app)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(request=request, name="routes/home/templates/index.html", context={"id": 2})
