from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.addresses.router import router as router_addresses
from src.auth.router import router as router_auth
from src.countries.router import router as router_countries
from src.payments.router import router as router_payments
from src.products.router import router as router_products
from src.users.router import router as router_users
from src.variations.router import router as router_variations


app = FastAPI()

origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://localhost:3000",
    "https://127.0.0.1:3000",
    "http://test",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_countries)
app.include_router(router_addresses)
app.include_router(router_payments)
app.include_router(router_products)
app.include_router(router_variations)
