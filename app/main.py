from fastapi import FastAPI
from app.api import endpoints

app = FastAPI()

# Include the API router
app.include_router(endpoints.router) 