from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)
app = FastAPI()


# instead of putting all the post and user routers in one main file. Split it into router folder
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hellodfdf dfdWorld"}



