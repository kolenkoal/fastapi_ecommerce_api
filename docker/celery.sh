#!/bin/bash

if [[ $1 == "celery" ]]; then
  celery --app=src.tasks.celery_settings:celery worker -l INFO -c 1
elif [[ $1 == "flower" ]]; then
  celery --app=src.tasks.celery_settings:celery flower
fi