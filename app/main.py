import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import Base, engine,test_db
from app import models  # import models before create_all
from app.routers import members, fund, loans, expenses, dashboard,fund_contribution

test_db()
Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Village Finance Management API",
    description="API for members, community fund transactions, loans, interest and expenses.",
    version="1.0.0",
    lifespan=lifespan,
)

origins = [x.strip() for x in os.getenv("FRONTEND_ORIGINS", "http://localhost:5173,http://127.0.0.1:5173").split(",") if x.strip()]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(members.router)
app.include_router(fund.router)
app.include_router(loans.router)
app.include_router(expenses.router)
app.include_router(dashboard.router)
app.include_router(fund_contribution.router)

@app.get("/")
def root():
    return {"message": "Village Finance Management API is running", "docs": "/docs"}

@app.get("/health")
def health():
    return {"status": "ok"}

