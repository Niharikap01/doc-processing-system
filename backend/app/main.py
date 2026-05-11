from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import router
from app.core.database import Base, engine
from app.core.redis_listener import listener

import asyncio

# create tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# routes
app.include_router(router)


# ---------------- STARTUP ----------------
@app.on_event("startup")
async def startup_event():
    # start redis websocket listener
    asyncio.create_task(listener.start())

    print("Redis Listener Started")