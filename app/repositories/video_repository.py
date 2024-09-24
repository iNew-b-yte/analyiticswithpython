from sqlalchemy.orm import Session
from app.models.video import Video
from app.schemas.video_schemas import VideoCreate
from app.interfaces.video_repository_interface import IVideoRepository
import logging

logger = logging.getLogger(__name__)

class VideoRepository(IVideoRepository):
    
    def get_video_by_id(self, db: Session, video_id: str) -> Video:
        """
        Returns a video by its video_id from the database.
        Logs the operation and errors, if any.
        """
        try:
            video = db.query(Video).filter(Video.video_id == video_id).first()
            if video:
                logger.info(f"Fetched video: {video_id}")
            return video
        except Exception as e:
            logger.error(f"Error fetching video by ID {video_id}: {e}")
            return None

    def get_videos(self, db: Session, skip: int = 0, limit: int = 10) -> list[Video]:
        """
        Retur a list of videos from the database.
        Supports pagination using skip and limit.
        Logs the operation and any potential errors.
        """
        try:
            videos = db.query(Video).offset(skip).limit(limit).all()
            logger.info(f"Fetched {len(videos)} videos.")
            return videos
        except Exception as e:
            logger.error(f"Error fetching videos: {e}")
            return []

    def create_video(self, db: Session, video: VideoCreate) -> Video:
        """
        Creates a new video entry in the database.
        Logs the operation and errors, if any.
        """
        try:
            db_video = Video(
                title=video.title,
                views=video.views,
                likes=video.likes,
                dislikes=video.dislikes,
                comment_count=video.comment_count,
                video_id=video.video_id,
            )
            db_video.engagement_rate = db_video.compute_engagement_rate()
            db.add(db_video)
            db.commit()
            db.refresh(db_video)
            logger.info(f"Created video with ID {video.video_id}")
            return db_video
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating video: {e}")
            return None
