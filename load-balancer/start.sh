#!/bin/bash
uvicorn load_balancer:app --host 0.0.0.0 --port 10000
