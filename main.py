## Packages required
from fastapi.staticfiles import StaticFiles

from fastapi import FastAPI
from routes import decider

def get_app() -> FastAPI:
    app = FastAPI(
        title = "Decide what to EAT"
        )
    
    app.mount("/static", StaticFiles(directory="static"), name="static")
    app.include_router(decider)

    return app

decider = get_app()