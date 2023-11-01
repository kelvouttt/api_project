from fastapi import FastAPI, Response
from fastapi import Form
import googlemaps
import os
import orjson

### API_KEY from environment variable
api_key = os.environ.get("API_KEY")
map_client = googlemaps.Client(api_key)

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

## Defining function
def get_details(restaurant_name):

    response = map_client.places(query=restaurant_name)

    format = response["results"][0]

    restaurant_name = format["name"]
    address = format["formatted_address"]
    open_now = format["opening_hours"].get("open_now")
    rating = format["rating"]
    return {"Restaurant name": restaurant_name, "Address": address, "Open": open_now, "Rating": rating}

@decider.get("/restaurant/{restaurant_name}", response_class=CustomORJSONResponse)
async def get_restaurant(restaurant_name):
    return get_details(restaurant_name)

@decider.post("/submit/{restaurant_name}", response_class=CustomORJSONResponse)
async def submit(Restaurant: str = Form()):
    return get_details(Restaurant)

# @decider.get("/")
# async def myself():
#     return {"hello, my name is Kelvin."}