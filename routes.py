from dataclasses import dataclass
from fastapi import Depends, Form, Response, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import orjson
import function.random_points as rp
import function.restaurants as details

decider = APIRouter()


templates = Jinja2Templates(directory="templates")

@dataclass
class Restaurant:
    name: str = Form(...)


## Defining JSON Response object
class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)

### Routes

## Will return whatever places we pass into the query parameters
@decider.get("/restaurant/{places_to_eat}", 
             response_class=CustomORJSONResponse)
async def get_restaurant(places_to_eat):
    return details.return_restaurant(places_to_eat)  

## We can submit a form, and it will return place details we put in
@decider.post("/submit/", response_class=HTMLResponse)
async def submit(request: Request, restaurant: Restaurant = Depends()):
    results_function: dict = details.response(restaurant)

    return templates.TemplateResponse("response.html", {"request": request,
                                                        "restaurant_name": results_function["Restaurant name"],
                                                        "address": results_function["Address"],
                                                        "status": results_function["Open"],
                                                        "rating": results_function["Rating"]      
                                                        })

## Will get new restaurants every refresh but response is in JSON format
@decider.get("/restaurantsJSON", 
             response_class=CustomORJSONResponse)
async def get_restaurant():
    return details.get_details()

## Return restaurants every refresh and response in HTMl page
@decider.post("/restaurants", 
             response_class=HTMLResponse)
async def get_restaurant(request: Request):
    random_restaurant: dict = details.get_details()

    static_api = details.static_api_key

    return templates.TemplateResponse("response.html", {"request": request,
                                                        "restaurant_name": random_restaurant["Restaurant name"],
                                                        "address": random_restaurant["Address"],
                                                        "status": random_restaurant["Open"],
                                                        "rating": random_restaurant["Rating"],
                                                        "static_api": static_api     
                                                        })

# @decider.get("/")
# async def myself():
#     return {"hello, my name is Kelvin."}