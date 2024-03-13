#!/bin/bash

alembic upgrade head

python3 src/utils/launch.py

python3 src/utils/insert_data.py

gunicorn src.app:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000