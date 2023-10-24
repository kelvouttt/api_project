from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from routes import router, router2
import googlemaps
import os
import orjson

# API_KEY from environment variable
api_key = os.environ.get("API_KEY")
map_client = googlemaps.Client(api_key)

# Initializing FastAPI as decider
decider = FastAPI(
    title="Decide what to EAT"
)

# Mounting the main.py to a static folder which has the css configuration
decider.mount("/static", StaticFiles(directory="static"), name="static")
decider.include_router(router)
decider.include_router(router2)


class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)


location_name = "eskrim angie"


def get_details(restaurant_name):
    response = map_client.places(query=location_name)
    restaurant_name = response["results"][0]["name"]
    address = response["results"][0]["formatted_address"]
    open_now = response["results"][0]["opening_hours"].get("open_now")
    rating = response["results"][0]["rating"]
    return {"Restaurant name": restaurant_name, "Address": address, "Open": open_now, "Rating": rating}


@decider.get("/", response_class=CustomORJSONResponse)
async def get_restaurant():
    return get_details(location_name)
