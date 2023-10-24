# This is a routes script which directs the request
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

# Initializaing a Jinja template object and pointing out to a template directory
templates = Jinja2Templates(directory="templates")
router = APIRouter()
router2 = APIRouter()


@router.get("/hello")
def index(request: Request):
    return templates.TemplateResponse("main.html",
                                      {"request": request,
                                       "name": "Kelvin",
                                       "age": 25})


@router2.get("/me")
async def myself():
    return {"Hello, my name is Kelvin."}
