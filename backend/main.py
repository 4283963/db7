from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from database import init_db, get_monthly_stats, get_weekday_stats

app = FastAPI(title="社群签到统计工具")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class MonthlyItem(BaseModel):
    month: str
    total: int


class MonthlyResponse(BaseModel):
    data: list[MonthlyItem]


class WeekdayItem(BaseModel):
    weekday: int
    weekday_name: str
    total: int


class WeekdayResponse(BaseModel):
    data: list[WeekdayItem]


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/api/stats/monthly", response_model=MonthlyResponse)
def monthly_stats(year: Optional[int] = None):
    return {"data": get_monthly_stats(year=year)}


@app.get("/api/stats/weekday", response_model=WeekdayResponse)
def weekday_stats(year: Optional[int] = None):
    return {"data": get_weekday_stats(year=year)}
