from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import video_router
from app.database.database import engine
from app.models.video import Base

# Initialize the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="YouTube Analytics App")

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal Server Error"}
    )

# Include the video routes
app.include_router(video_router.router, prefix="/api")
