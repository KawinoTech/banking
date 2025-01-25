"""
Main Module for the FastAPI Application.

This module serves as the entry point for the application. It initializes the FastAPI app, 
configures middleware, includes routers for various functionalities, and sets up periodic 
tasks using a background scheduler.

Key Responsibilities:
----------------------
1. **Application Initialization**:
   - Creates the FastAPI app instance.
   - Configures middleware for CORS and rate limiting.

2. **Database Setup**:
   - Initializes database models by creating tables based on ORM definitions.

3. **Route Inclusion**:
   - Includes routers for user management, transactions, loans, term deposits, cards, 
     help desk, and new account operations.

4. **Scheduled Tasks**:
   - Sets up and manages a background scheduler to run periodic tasks, such as calculating 
     interest for loans and term deposits.

5. **Startup and Shutdown Events**:
   - Handles resource initialization (e.g., Redis connection) on startup.
   - Cleans up resources (e.g., shutting down the scheduler) on shutdown.

Application Middleware:
-----------------------
- **CORS Middleware**:
  Allows cross-origin requests. Currently configured to allow all origins 
  (should be restricted in production environments).

- **Rate Limiting**:
  Configured using FastAPI-Limiter and Redis to protect endpoints from abuse.

Routers Included:
-----------------
- **users.router**: User management operations (e.g., authentication, profile updates).
- **transactions.router**: Handles all transaction-related functionality.
- **loans.router**: Manages loan operations.
- **termdeposits.router**: Handles term deposit-related operations.
- **cards.router**: Manages credit and debit card functionality.
- **help_desk.router**: Routes for customer support/help desk interactions.
- **new_account.router**: Facilitates the creation of new accounts.

Background Scheduler:
----------------------
Uses APScheduler to manage periodic tasks:
- **Loan Interest Calculation**: Calculates interest on active loans daily.
- **Term Deposit Interest Calculation**: Calculates interest on term deposits daily.

Redis Integration:
------------------
- Redis is used for rate limiting with the FastAPI-Limiter library. Ensure Redis is running 
  and accessible at the configured `redis://localhost` endpoint.

Notes:
------
- Avoid using `allow_origins = ['*']` in production; restrict it to trusted origins.
- Periodic tasks should be reviewed for correctness and scalability when dealing with a 
  large dataset.

"""


from fastapi import FastAPI
from .routes import users, transactions, new_account, help_desk, cards, termdeposits, loans
from fastapi.middleware.cors import CORSMiddleware
from .database import engine
from fastapi_limiter import FastAPILimiter
import redis.asyncio as aioredis
from apscheduler.schedulers.background import BackgroundScheduler
from .schedules import calculate_interest_for_loans, calculate_interest_for_tds
from .models import Base

# Create all database tables defined in the models
Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI()

# Initialize the background scheduler for periodic tasks
scheduler = BackgroundScheduler()


@app.on_event("startup")
async def startup():
    """
    Event handler triggered when the FastAPI application starts.

    This function performs the following:
    - Initializes the Redis client for use with the FastAPI Limiter middleware for rate limiting.
    - Starts the background scheduler and adds periodic tasks to calculate interest for loans
      and term deposits.
    """
    # Initialize Redis connection for rate limiting
    redis = await aioredis.from_url("redis://localhost", encoding="utf-8", decode_responses=True)
    await FastAPILimiter.init(redis)

    # Add periodic tasks to the scheduler
    scheduler.add_job(
        calculate_interest_for_loans,
        "interval",
        days=1,
        id="loan_interest_job",
        replace_existing=True,  # Avoid duplicate jobs
    )
    scheduler.add_job(
        calculate_interest_for_tds,
        "interval",
        days=1,
        id="td_interest_job",
        replace_existing=True,  # Avoid duplicate jobs
    )

    # Start the scheduler
    scheduler.start()


@app.on_event("shutdown")
def shutdown_event():
    """
    Event handler triggered when the FastAPI application shuts down.

    This function performs the following:
    - Gracefully shuts down the background scheduler to ensure all scheduled jobs
      are properly terminated.
    """
    scheduler.shutdown()


# Include application routers for various functionalities
app.include_router(transactions.router)
app.include_router(loans.router)
app.include_router(termdeposits.router)
app.include_router(cards.router)
app.include_router(help_desk.router)
app.include_router(users.router)
app.include_router(new_account.router)

# Configure CORS middleware
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allow all origins (should be restricted in production)
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

"""
Routers Included:
- transactions.router: Handles operations related to transactions.
- loans.router: Manages loan-related operations.
- termdeposits.router: Handles term deposit functionalities.
- cards.router: Manages credit/debit card-related operations.
- help_desk.router: Provides routes for customer support or help desk operations.
- users.router: Handles user management such as authentication and profile updates.
- new_account.router: Facilitates the creation of new accounts.
"""
