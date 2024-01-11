import os
import sys

from fastapi import FastAPI


sys.path.insert(1, os.path.join(sys.path[0], ".."))

app = FastAPI()


@app.get("/")
def hello():
    return {"hello": "world"}
