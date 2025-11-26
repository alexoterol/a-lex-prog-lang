#!/usr/bin/env bash

echo "Starting frontend"
python -m http.server 5500 --directory ./src/frontend &

echo "Starting backend"
cd src && uvicorn server.app:app --port 8000

