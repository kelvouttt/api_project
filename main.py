from fastapi import FastAPI, Response
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

class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)

location_name = "dera uma"

def get_details(restaurant_name):

    response = map_client.places(query=location_name)

    format = response["results"][0]

    restaurant_name = format["name"]
    address = format["formatted_address"]
    open_now = format["opening_hours"].get("open_now")
    rating = format["rating"]
    return {"Restaurant name": restaurant_name, "Address": address, "Open": open_now, "Rating": rating}

@decider.get("/", response_class=CustomORJSONResponse)
async def get_restaurant():
    return get_details(location_name)

@decider.get("/me")
async def myself():
    return {"hello, my name is Kelvin."}