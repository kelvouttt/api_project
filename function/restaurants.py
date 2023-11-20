import googlemaps
import os
from function import get_coordinates as gc


### API_KEY from environment variable
api_key = os.environ.get("API_KEY")
map_client = googlemaps.Client(api_key)

## Defining function to parse the restaurant details
def get_details():

    response = map_client.places(type="restaurant", location=gc.get_coordinates())
    format = response["results"][0]

    restaurant_name = format["name"]
    address = format["formatted_address"]
    open_now = format["opening_hours"].get("open_now")
    rating = format["rating"]
    location = format["geometry"]
    return {"Restaurant name": restaurant_name, "Address": address, "Open": open_now, "Rating": rating, "Location": location}

def return_restaurant(restaurant_name):

    response = map_client.places(query=restaurant_name)

    format = response["results"][0]

    restaurant_name = format["name"]
    address = format["formatted_address"]
    open_now = format["opening_hours"].get("open_now")
    rating = format["rating"]
    return {"Restaurant name": restaurant_name, "Address": address, "Open": open_now, "Rating": rating}

def response(restaurant_name: str):
    response = map_client.places(query=restaurant_name)

    format = response["results"][0]

    restaurant_name = format["name"]
    address = format["formatted_address"]
    open_now = format["opening_hours"].get("open_now")
    rating = format["rating"]

    return {"Restaurant name": restaurant_name, "Address": address, "Open": open_now, "Rating": rating}