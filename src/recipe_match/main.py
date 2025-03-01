from fastapi import FastAPI
from recipe_match.routes import recipe_router

# Initialize the FastAPI application
app = FastAPI(
    title="Recipe Match API",
    description="An API for finding recipes based on available ingredients",
    version="0.1.0"
)

# Include routers
app.include_router(recipe_router)

@app.get("/")
async def root():
    """Root endpoint to confirm the API is running."""
    return {"message": "Recipe Match API is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("recipe_match.main:app", host="0.0.0.0", port=8000, reload=True)
