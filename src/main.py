import os
import sys

import uvicorn
from fastapi import FastAPI

from src.auth.router import router as router_auth
from src.users.router import router as router_users


sys.path.insert(1, os.path.join(sys.path[0], ".."))

app = FastAPI()

app.include_router(router_auth)
app.include_router(router_users)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
