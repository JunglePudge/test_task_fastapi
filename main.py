from fastapi import FastAPI
from api import router
from external import fake_api


app = FastAPI()
app.mount("/external", fake_api)
app.include_router(router)