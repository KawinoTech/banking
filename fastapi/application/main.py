from fastapi import FastAPI
from .routes import users, transactions, new_account, help_desk, cards, termdeposits, loans
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from fastapi_limiter import FastAPILimiter
import redis.asyncio as aioredis
from apscheduler.schedulers.background import BackgroundScheduler
from .schedules import calculate_interest_for_loans


#creates all our models/ Though Alembic is an alternativeLll

from .models import accounts

accounts.Base.metadata.create_all(bind=engine)
app = FastAPI()
@app.on_event("startup")
async def startup():
    redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)
@app.on_event("startup")
def startup_event():
    scheduler = BackgroundScheduler()
    scheduler.add_job(calculate_interest_for_loans, 'interval', minutes=1)
    scheduler.start()

@app.on_event("shutdown")
def shutdown_event():
    scheduler.shutdown()

app.include_router(transactions.router)
app.include_router(loans.router)
app.include_router(termdeposits.router)
app.include_router(cards.router)
app.include_router(help_desk.router)
app.include_router(users.router)
app.include_router(new_account.router)
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_headers = ['*'],
    allow_methods = ['*']
)








