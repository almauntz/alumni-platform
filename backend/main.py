from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import create_db_and_tables
from routers import alumni, external

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(alumni.router, prefix="/api/alumni", tags=["alumni"])
app.include_router(external.router, prefix="/api/external", tags=["external"])


@app.on_event("startup")
def on_startup():
    create_db_and_tables()
