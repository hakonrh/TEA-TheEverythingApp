#!/bin/bash

alembic revision --autogenerate -m "Drop followers and like tables, add likes column to posts"
alembic upgrade head
uvicorn main:app --host 0.0.0.0 --port 10000
