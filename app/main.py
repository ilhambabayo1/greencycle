from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.database import Base, engine
from app.routers import items, pages


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="GreenCycle", lifespan=lifespan)

app.include_router(pages.router)
app.include_router(items.router)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
