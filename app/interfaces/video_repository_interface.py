from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from app.schemas.video_schemas import VideoCreate
from app.models.video import Video

class IVideoRepository(ABC):
    @abstractmethod
    def get_video_by_id(self, db: Session, video_id: str) -> Video:
        pass

    @abstractmethod
    def get_videos(self, db: Session, skip: int, limit: int) -> list[Video]:
        pass

    @abstractmethod
    def create_video(self, db: Session, video: VideoCreate) -> Video:
        pass
