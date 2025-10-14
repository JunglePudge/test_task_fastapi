from fastapi import FastAPI
from app.api.api import router
from app.api.external import fake_api


app = FastAPI()
app.mount("/external", fake_api)
app.include_router(router)