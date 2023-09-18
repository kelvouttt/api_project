from fastapi import FastAPI
import googlemaps
import os

decider = FastAPI(
    title = "Decide what to EAT"
)

api_key = os.environ.get("API_KEY")
map_client = googlemaps.Client(api_key)

def get_details(restaurant_name):
    response = map_client.places(query=location_name)
    restaurant_name = response["results"][0]["name"]
    address = response["results"][0]["formatted_address"]
    open_now = response["results"][0]["opening_hours"].get("open_now")
    rating = response["results"][0]["rating"]
    return {"Restaurant name": restaurant_name, "Address": address, "Open": open_now, "Rating": rating}

location_name = "Oiden"

@decider.get("/")
async def getRestaurant():
    return get_details(location_name)

@decider.get("/me")
async def myself():
    return {"hello, my name is Kelvin."}