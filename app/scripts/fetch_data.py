import csv
import logging
from fastapi import Depends
from sqlalchemy.orm import Session
from app.schemas.video_schemas import VideoCreate
from app.database.database import sql_db
from app.repositories.video_repository import VideoRepository
# from app.interfaces.video_repository_interface import IVideoRepository
# from app.dependencies.video_dependencies import get_video_repository

# Initialize logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_data_into_db():
    """
    Loads trending YouTube video data from a CSV file into the SQLite database.
    Logs the errors and progress.
    """
    video_repository = VideoRepository()
    db: Session = next(sql_db())
    try:
        print("Loading data into the database...")
        with open('data/trending_videos.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(f"Processing video {row['video_id']}")
                video_data = VideoCreate(
                    title=row['title'],
                    views=int(row['views']),
                    likes=int(row['likes']),
                    dislikes=int(row['dislikes']),
                    comment_count=int(row['comment_count']),
                    video_id=row['video_id']
                )
                created_video = video_repository.create_video(db=db, video=video_data)
                if created_video:
                    logger.info(f"Inserted video {created_video.video_id}")
                else:
                    logger.error(f"Failed to insert video {row['video_id']}")
        logger.info("Data loading completed.")
    except Exception as e:
        logger.critical(f"Error loading data into the database: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    load_data_into_db()
