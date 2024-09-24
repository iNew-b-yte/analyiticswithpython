from app.repositories.video_repository import VideoRepository
from app.interfaces.video_repository_interface import IVideoRepository

def get_video_repository() -> IVideoRepository:
    return VideoRepository()  # Return the concrete implementation
