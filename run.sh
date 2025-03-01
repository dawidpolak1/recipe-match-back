#!/bin/bash
PYTHONPATH=$(pwd)/src poetry run uvicorn recipe_match.main:app --reload 