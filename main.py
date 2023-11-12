## Packages required
from fastapi import FastAPI, Response
from fastapi import Form
import googlemaps
import os
import orjson
import random
import numpy as np
from shapely.geometry import Polygon, Point

### API_KEY from environment variable
api_key = os.environ.get("API_KEY")
map_client = googlemaps.Client(api_key)

### Initializing FastAPI as decider
decider = FastAPI(
    title = "Decide what to EAT"
)

## Define desired Polygon
# https://medium.com/the-data-journal/a-quick-trick-to-create-random-lat-long-coordinates-in-python-within-a-defined-polygon-e8997f05123a
poly = Polygon([(-33.822218,151.084762), 
                (-33.919981,151.099747),
                (-33.917772,151.240542),
                (-33.872596, 151.262135)])

## Define the randomizer function using NumPy
def polygon_random_points(poly, num_points):
    min_x, min_y, max_x, max_y = poly.bounds

    points = []
    while len(points) < num_points:
        random_point = Point([random.uniform(min_x, max_x),
                            random.uniform(min_y, max_y)])
        if (random_point.within(poly)):
            points.append(random_point)
    # This function will return a list with only 1 length, the next function will split this up into coordinate x and coordinate y.
    return points

## Get coordinate x and y
def get_coordinates():
    location = polygon_random_points(poly, 1)
    # The way it was done is by returning both coordinates.
    for coordinates in location:
        print(coordinates.x, coordinates.y)
        return coordinates.x, coordinates.y

get_coordinates()

## Defining JSON Response object
class CustomORJSONResponse(Response):
    media_type = "application/json"

    def render(self, content: any) -> bytes:
        assert orjson is not None, "orjson must be installed"
        return orjson.dumps(content, option=orjson.OPT_INDENT_2)


## Defining function to parse the restaurant details
def get_details():

    response = map_client.places(type="restaurant", location=get_coordinates())
    # print(response)
    format = response["results"][0]

    restaurant_name = format["name"]
    address = format["formatted_address"]
    open_now = format["opening_hours"].get("open_now")
    rating = format["rating"]
    location = format["geometry"]
    return {"Restaurant name": restaurant_name, "Address": address, "Open": open_now, "Rating": rating, "Location": location}

@decider.get("/restaurant/{places_to_eat}", 
             response_class=CustomORJSONResponse)
async def get_restaurant(places_to_eat):
    return get_details(places_to_eat)

@decider.post("/submit/{restaurant_name}", response_class=CustomORJSONResponse)
async def submit(Restaurant: str = Form()):
    return get_details(Restaurant)

@decider.get("/restaurants", 
             response_class=CustomORJSONResponse)
async def get_restaurant():
    return get_details()

# @decider.get("/")
# async def myself():
#     return {"hello, my name is Kelvin."}

## TO DO: 
## The code above is somewhat working to randomize random coordinates. 

## The problem is that the coordinates being returned is longer than what Google API is taking.