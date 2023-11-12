## Packages required
from fastapi import FastAPI, Response
from fastapi import Form
import orjson
import random_points as rp
import get_details as details


### Initializing FastAPI as decider
decider = FastAPI(
    title = "Decide what to EAT"
)

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
    return details.get_details(places_to_eat)

@decider.post("/submit/{restaurant_name}", response_class=CustomORJSONResponse)
async def submit(Restaurant: str = Form()):
    return details.get_details(Restaurant)

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