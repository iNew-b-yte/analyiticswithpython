from sqlalchemy import Column, Integer, String, Float
from app.database.database import Base

class Video(Base):
    """
    Model for the YouTube Video table.
    Represents a video and its associated statistics like views, likes, and engagement rate.
    """
    __tablename__ = "youtube_videos"

    id = Column(Integer, primary_key=True, index=True)
    video_id = Column(String, unique=True, index=True)
    title = Column(String, index=True)
    views = Column(Integer)
    likes = Column(Integer)
    dislikes = Column(Integer)
    comment_count = Column(Integer)
    engagement_rate = Column(Float)

    def compute_engagement_rate(self):
        """
        Computes the engagement rate of a video based on its views, likes, and comment count.
        """
        # Engagement rate = (Likes + Comments) / Views
        if self.views > 0:
            return (self.likes + self.comment_count) / self.views
        return 0.0