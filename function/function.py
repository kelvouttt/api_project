import googlemaps
import os
from function import get_coordinates as gc


### API_KEY from environment variable
api_key = os.environ.get("API_KEY")
static_api_key = os.environ.get("API_KEY_STATIC")

map_client = googlemaps.Client(api_key)
static_map_client = googlemaps.Client(static_api_key)

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

## Getting the latitude and longitude based on the postcode input from the user
def input_response(postcode: int):
    response = static_map_client.geocode(components={
                                        "country": "AU","postal_code":postcode})
    format = response[0]
    location = format["geometry"]["location"]

    address = format["formatted_address"]
    lat = location["lat"]
    lng = location["lng"]
    
    return lat, lng

## This function will get the input from user in a form of postcode, the postcode will be the argument for the function input_response which takes a postal code and transform it into a latitude / longitude. 

## The lat / lng will be the argument for the location parameter in the .places() function. 
def get_place_from_postcode(postcode: int):
    response = map_client.places(type="restaurant", location=input_response(postcode), radius=10000)

    format = response["results"][0]

    restaurant_name = format["name"]
    address = format["formatted_address"]
    open_now = format["opening_hours"].get("open_now")
    rating = format["rating"]
    print(response)
    return {"Restaurant name": restaurant_name, "Address": address, "Open": open_now, "Rating": rating}