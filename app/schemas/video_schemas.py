from pydantic import BaseModel

class VideoBase(BaseModel):
    title: str
    views: int
    likes: int
    dislikes: int
    comment_count: int
    video_id: str

class VideoCreate(VideoBase):
    pass
    # video_id: str

class Video(VideoBase):
    id: int
    engagement_rate: float
    class Config:
        from_attributes = True
