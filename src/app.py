from fastapi import FastAPI

from src.auth.router import router as router_auth
from src.countries.router import router as router_countries
from src.users.router import router as router_users


app = FastAPI()

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_countries)
