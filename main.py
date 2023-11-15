## Packages required
from dataclasses import dataclass
from fastapi import Depends, FastAPI, Form, Response, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pydantic import BaseModel
from dataclasses import dataclass

import orjson
import random_points as rp
import restaurants as details


@dataclass
class Restaurant:
    name: str = Form(...)

### Initializing FastAPI as decider
decider = FastAPI(
    title = "Decide what to EAT"
)

templates = Jinja2Templates(directory="templates")

decider.mount("/static", StaticFiles(directory="static"), name="static")

## Defining JSON Response object
class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)

## Routes
@decider.get("/restaurant/{places_to_eat}", 
             response_class=CustomORJSONResponse)
async def get_restaurant(places_to_eat):
    return details.return_restaurant(places_to_eat)

@decider.post("/submit/", response_class=CustomORJSONResponse)
async def submit(restaurant: Restaurant = Depends()):
    return details.response(restaurant.name)

# @decider.get("/response")
# async def get_response(request: Request):
#     return templates.TemplateResponse("response.html", {'request': request})

@decider.get("/restaurants", 
             response_class=CustomORJSONResponse)
async def get_restaurant():
    return details.get_details()

# @decider.get("/")
# async def myself():
#     return {"hello, my name is Kelvin."}

## TO DO: 
## The code above is somewhat working to randomize random coordinates. 

## The problem is that the coordinates being returned is longer than what Google API is taking.