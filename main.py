from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from slowapi.middleware import SlowAPIMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from rate_limiter import limiter
from routes import router

app = FastAPI(
    title="Trade Opportunities API",
    description="Analyze trade opportunities by sector", 
    version="1.0.0"
)

# Attach the limiter to the app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

app.include_router(router)

@app.get("/")
async def root():
    return {"message": "Trade Opportunities API is running!"}
