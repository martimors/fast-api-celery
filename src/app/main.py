"""
Because of some magic behavior of FastAPI, this module MUST be app.main
and it must also have the app object defined here. Otherwise the docker
container running the app will not work.
"""

from fastapi import FastAPI
from app.routers.taskrouter import router as taskrouter


def create_fastapi_app():
    app = FastAPI()
    app.include_router(taskrouter)

    @app.get("/")
    def root():
        return {"message": "Hello Bigger Applications!"}

    return app


app = create_fastapi_app()