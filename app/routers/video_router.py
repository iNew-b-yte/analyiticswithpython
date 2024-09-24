import logging
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from app.schemas.video_schemas import VideoCreate, Video
from app.interfaces.video_repository_interface import IVideoRepository
from app.dependencies.video_dependencies import get_video_repository
from app.database.database import sql_db

router = APIRouter()
logger = logging.getLogger(__name__)

def background_task_update_data(video_id: str, db: Session = Depends(sql_db), video_repository: IVideoRepository = Depends(get_video_repository)):
    """
    Simulated background task to update video statistics.
    Logs the task start and end.
    """
    logger.info(f"Background task started for video {video_id}")
    video = video_repository.get_video_by_id(db, video_id=video_id)
    if video:
        video.engagement_rate = video.compute_engagement_rate()
        db.commit()
        logger.info(f"Background task completed for video {video_id}")
    else:
        logger.error(f"Video {video_id} not found in background task.")

@router.get("/videos/", response_model=list[Video])
def get_videos(skip: int = 0, limit: int = 10, 
                db: Session = Depends(sql_db), 
                video_repository: IVideoRepository = Depends(get_video_repository)):
    """
    Endpoint to retrieve videos with pagination.
    """
    videos = video_repository.get_videos(db=db, skip=skip, limit=limit)
    if not videos:
        raise HTTPException(status_code=404, detail="No videos found.")
    return videos

@router.post("/videos/", response_model=Video)
def create_video(video: VideoCreate, 
                 background_tasks: BackgroundTasks,
                 db: Session = Depends(sql_db),
                 video_repository: IVideoRepository = Depends(get_video_repository)):
    """
    Endpoint to create a new video.
    After creating the video, a background task is triggered to update the statistics.
    """
    existing_video = video_repository.get_video_by_id(db=db, video_id=video.video_id)
    if existing_video:
        raise HTTPException(status_code=400, detail="Video already registered")
    
    created_video = video_repository.create_video(db=db, video=video)
    if created_video:
        background_tasks.add_task(background_task_update_data, db, video.video_id)
        return created_video
    else:
        raise HTTPException(status_code=500, detail="Error creating video")

@router.get("/videos/{video_id}", response_model=Video)
def read_video(video_id: str, 
               db: Session = Depends(sql_db),
               video_repository: IVideoRepository = Depends(get_video_repository)):
    """
    Endpoint to retrieve a single video by its video_id.
    """
    try:
        video = video_repository.get_video_by_id(db=db, video_id=video_id)
        if not video:
            # Return 404 if the video is not found
            raise HTTPException(status_code=404, detail="Video not found")
        
        return video  # Return the video if found

    except HTTPException as http_exc:
        # Re-raise HTTPExceptions to let FastAPI handle them
        return JSONResponse(
            status_code= http_exc.status_code,
            content={"detail": http_exc.detail},
        )
    except Exception as e:
        logger.error(f"Error fetching video by ID {video_id}: {e}")
        # Return a 500 server error for any other exceptions
        return JSONResponse(
            status_code= 500,
            content={"detail": e.args[0]}
        )
