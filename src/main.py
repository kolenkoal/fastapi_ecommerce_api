import os
import sys

from fastapi import FastAPI

from src.auth.router import router as router_auth
from src.users.router import router as router_users


sys.path.insert(1, os.path.join(sys.path[0], ".."))

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_users)
