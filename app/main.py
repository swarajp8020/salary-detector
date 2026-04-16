from fastapi import FastAPI
from app.api.salary_api import router

app = FastAPI(title="Salary Detection Service")

app.include_router(router)