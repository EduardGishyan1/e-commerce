from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

from fastapi import FastAPI, status
from fastapi.responses import RedirectResponse

from app.models.base import Base
from app.database.session import engine, initialize_db
from app.routers.wishlists import router as wishlists_router
from app.middleware.rate_limitter import AdvancedMiddleware
from app.routers import (auth, users, products, orders, password_recovery,
                         admin, payments, order_item, reviews, cart_items)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await initialize_db()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield

app = FastAPI(lifespan=lifespan)

@app.get('/')
async def redirect_home():
    response = RedirectResponse(status_code=status.HTTP_301_MOVED_PERMANENTLY, url='/docs')
    return response

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,       # Frontend URLs
    allow_credentials=True,      # Needed if you use cookies
    allow_methods=["*"],         # Allow POST, GET, PUT, DELETE, etc.
    allow_headers=["*"],         # Allow headers like Content-Type
)

app.include_router(auth.router)
app.include_router(password_recovery.router)
app.include_router(admin.router)
app.include_router(users.router)
app.include_router(products.router)
app.include_router(cart_items.router)
app.include_router(orders.router)
app.include_router(order_item.router)
app.include_router(payments.router)
app.include_router(reviews.router)
app.include_router(wishlists_router)
app.add_middleware(AdvancedMiddleware)