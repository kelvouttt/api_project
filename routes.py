from dataclasses import dataclass
from fastapi import Depends, Form, Response, Request, APIRouter
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from function import function as details
from typing_extensions import Annotated

import orjson
import function.random_points as rp


decider = APIRouter()


templates = Jinja2Templates(directory="templates")

@dataclass
class Restaurant:
    name: str = Form(...)

# Creating a new class for postal code post request, for some reason, I can't instantiate new object using the existing class Restaurant. So as a workaround, will try to create new object instead to make it work.
# @dataclass 
# class Postal:
#     postcode: int = Form(...)


## Defining JSON Response object
class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)

### Routes

# Will return whatever places we pass into the query parameters
@decider.get("/restaurant/{places_to_eat}", 
             response_class=CustomORJSONResponse)
async def get_restaurant(places_to_eat):
    return details.return_restaurant(places_to_eat) 

## We can submit a form, and it will return place details we put in
@decider.post("/submit/", 
              response_class=HTMLResponse)
async def submit(request: Request, restaurant: Restaurant = Depends()):
    results_function: dict = details.response(restaurant)

    return templates.TemplateResponse("submit_response.html", {"request": request,
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
@decider.post("/restaurants/", 
             response_class=HTMLResponse)
async def get_restaurant(request: Request):
    random_restaurant: dict = details.get_details()

    static_api = details.static_api_key

    return templates.TemplateResponse("response.html", {"request": request,
                                                        "restaurant_name": random_restaurant["Restaurant name"],
                                                        "address": random_restaurant["Address"],
                                                        "status": random_restaurant["Open"],
                                                        "rating": random_restaurant["Rating"],
                                                        ## This static API is being called out in response.html to avoid hard-coding the API key in this file
                                                        "static_api": static_api     
                                                        })

# Right now, I am using Annotated and form feature from FastAPI to make the post request work - I have tried creating the class Postal as above, but it didn't work as the error seems to be pointing to a validation error where required fields are missing (although I'm not sure what's really missing)
@decider.post("/postalcode/", 
              response_class=HTMLResponse)
async def submit_form(request: Request, postalcode: Annotated[int, Form()]):
    function_result: dict = details.input_response(postalcode)
    print(function_result["Address"])
    return templates.TemplateResponse("postal_response.html", {"request": request,
                                                            "address": function_result["Address"]    
                                                            })


@decider.get("/postal/{postcode}", 
             response_class=CustomORJSONResponse)
async def get_restaurant(postcode):
    return details.input_response(postcode)  
 
# @decider.get("/")
# async def myself():
#     return {"hello, my name is Kelvin."}