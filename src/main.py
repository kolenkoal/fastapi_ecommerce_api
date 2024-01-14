import os
import sys

import uvicorn


sys.path.insert(1, os.path.join(sys.path[0], ".."))

from src.app import app  # noqa


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
