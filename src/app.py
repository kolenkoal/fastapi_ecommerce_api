from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from src.addresses.router import router as router_addresses
from src.auth.router import router as router_auth
from src.countries.router import router as router_countries
from src.images.router import router as router_images
from src.orders.router import router as router_orders
from src.payments.router import router as router_payments
from src.products.router import router as router_products
from src.shipping_methods.router import router as router_shipping_methods
from src.shopping_carts.router import router as router_shopping_carts
from src.users.router import router as router_users
from src.variation_options.router import router as router_variation_options
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

app.mount("/static", StaticFiles(directory="src/static"), "static")

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_countries)
app.include_router(router_addresses)
app.include_router(router_payments)
app.include_router(router_variations)
app.include_router(router_variation_options)
app.include_router(router_products)
app.include_router(router_images)
app.include_router(router_shopping_carts)
app.include_router(router_shipping_methods)
app.include_router(router_orders)
