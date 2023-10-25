import subprocess
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles

from routes import router, router2

from config import Settings
from crud import CRUD

import googlemaps
import os
import orjson

# API_KEY from environment variable
api_key = os.environ.get("API_KEY")
map_client = googlemaps.Client(api_key)

settings = Settings()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Context manager for FastAPI app. It will run all code before `yield`
    on app startup, and will run code after `yeld` on app shutdown.
    """

    try:
        subprocess.run([
            "tailwindcss",
            "-i",
            str(settings.STATIC_DIR / "src" / "input.css"),
            "-o",
            str(settings.STATIC_DIR / "main.css"),
        ])
    except Exception as e:
        print(f"Error running tailwindcss: {e}")

    yield

def get_app() -> FastAPI:
    """Create a FastAPI app with the specified settings."""
    app = FastAPI(
        lifespan=lifespan,
        **settings.fastapi_kwargs)
    
    # Mounting the main.py to a static folder which has the css configuration
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(router)
    app.include_router(router2)

    return app

decider = get_app()

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(decider, host="127.0.0.1", port=8000)

# class CustomORJSONResponse(Response):
#     media_type = "application/json"

#     def render(self, content: any) -> bytes:
#         assert orjson is not None, "orjson must be installed"
#         return orjson.dumps(content, option=orjson.OPT_INDENT_2)


# location_name = "eskrim angie"


# def get_details(restaurant_name):
#     response = map_client.places(query=location_name)
#     restaurant_name = response["results"][0]["name"]
#     address = response["results"][0]["formatted_address"]
#     open_now = response["results"][0]["opening_hours"].get("open_now")
#     rating = response["results"][0]["rating"]
#     return {"Restaurant name": restaurant_name, "Address": address, "Open": open_now, "Rating": rating}


# @decider.get("/", response_class=CustomORJSONResponse)
# async def get_restaurant():
#     return get_details(location_name)
