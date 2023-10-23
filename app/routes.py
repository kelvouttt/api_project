from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates")
router = APIRouter()

@router.get("/hello")
def index(request: Request):
  return templates.TemplateResponse("shared/_base.html", 
                                    {"request": request})

@router.get("/me")
async def myself():
    return {"Hello, my name is Kelvin."}