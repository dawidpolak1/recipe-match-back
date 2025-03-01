import os
import sys
import subprocess

def run_app():
    """Run the FastAPI application with the correct PYTHONPATH."""
    # Add the src directory to the PYTHONPATH
    src_path = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    if src_path not in sys.path:
        sys.path.insert(0, src_path)
        
    # Run uvicorn
    from uvicorn import run
    run("recipe_match.main:app", host="0.0.0.0", port=8000, reload=True) 