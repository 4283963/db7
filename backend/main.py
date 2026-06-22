from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db, get_monthly_stats, get_weekday_stats

app = FastAPI(title="社群签到统计工具")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def on_startup():
    init_db()


@app.get("/api/stats/monthly")
def monthly_stats():
    return {"data": get_monthly_stats()}


@app.get("/api/stats/weekday")
def weekday_stats():
    return {"data": get_weekday_stats()}
