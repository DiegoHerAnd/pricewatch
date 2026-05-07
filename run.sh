#!/bin/bash
source venv/bin/activate
PYTHONPATH=. uvicorn app.main:app --reload
