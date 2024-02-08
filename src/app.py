from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.addresses.router import router as router_addresses
from src.auth.router import router as router_auth
from src.countries.router import router as router_countries
from src.payments.payment_types.router import router as router_payment_types
from src.payments.user_payment_methods.router import (
    router as router_payment_methods,
)
from src.users.router import router as router_users


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
app.include_router(router_payment_types)
app.include_router(router_payment_methods)
