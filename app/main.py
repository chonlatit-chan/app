from fastapi import FastAPI
from .routers import form, user

app = FastAPI()


app.include_router(form.router)
app.include_router(user.router)


@app.get("/")
async def root():
    return {"message": "Welcome!!"}

