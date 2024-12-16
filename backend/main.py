from fastapi import FastAPI

from database import Base, engine
from routes.configurations import config_router
from routes.user import user_router

app = FastAPI()
app.include_router(user_router, prefix='/user')
app.include_router(config_router)

Base.metadata.create_all(bind=engine)