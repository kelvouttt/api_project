# This is a routes script which directs the request
from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from config import Settings
from crud import CRUD

settings = Settings()
# Initializaing a Jinja template object and pointing out to a template directory
templates = Jinja2Templates(directory=settings.TEMPLATE_DIR)
router = APIRouter()
router2 = APIRouter()


@router.get("/hello")
def hello(request: Request):
    return templates.TemplateResponse("shared/_base.html",
                                      {"request": request,
                                       "name": "Kelvin",
                                       "age": 25})

@router.get("/test")
def index(request: Request):

    db = CRUD().with_table("artist_info")
    random_artist = db.get_random_item()

    return templates.TemplateResponse(
        "main.html",
        {
            "request": request,
            "random_artist": random_artist})


@router2.get("/me")
def myself():
    return "Hello, my name is Kelvin."
