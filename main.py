from fastapi import FastAPI

from app.db.database import engine, Base
from app.routes import auth, post

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(post.router)


@app.get("/")
def read_root():
    return {"message": "This is simple assessment for lucidtask"}
