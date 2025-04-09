from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recipe_match.routes import recipe_router, detailed_recipes_router

# Initialize the FastAPI application
app = FastAPI(
    title="Recipe Match API",
    description="An API for finding recipes based on available ingredients",
    version="0.1.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    # Allow requests from your frontend origin
    allow_origins=["http://localhost:5173"],
    # Optionally allow requests from other origins in different environments
    # allow_origins=["*"],  # Use this during development if needed, but not in production
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Include routers
app.include_router(recipe_router)
app.include_router(detailed_recipes_router)

@app.get("/")
async def root():
    """Root endpoint to confirm the API is running."""
    return {"message": "Recipe Match API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("recipe_match.main:app", host="0.0.0.0", port=8000, reload=True)
