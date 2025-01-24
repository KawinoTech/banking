from fastapi import FastAPI
from .routes import users, transactions, new_account, help_desk, cards, termdeposits, loans
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from fastapi_limiter import FastAPILimiter
import redis.asyncio as aioredis
from apscheduler.schedulers.background import BackgroundScheduler
from .schedules import calculate_interest_for_loans, calculate_interest_for_tds


#creates all our models/ Though Alembic is an alternativeLll

from .models import accounts

accounts.Base.metadata.create_all(bind=engine)
app = FastAPI()
# Initialize and start the background scheduler for interest calculations
scheduler = BackgroundScheduler()
# Event triggered when the FastAPI app starts
@app.on_event("startup")
async def startup():
    """
    Initializes the Redis client for rate limiting and starts the background scheduler
    for periodic interest calculations on loans and term deposits.
    """
    # Initialize Redis connection
    redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)

    scheduler.add_job(calculate_interest_for_loans, 'interval', days=1, id="loan_interest_job")
    scheduler.add_job(calculate_interest_for_tds, 'interval', days=1, id="td_interest_job")
    scheduler.start()

# Event triggered when the FastAPI app shuts down
@app.on_event("shutdown")
def shutdown_event():
    """
    Shuts down the background scheduler when the app shuts down.
    """
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








