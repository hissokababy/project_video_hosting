from typing import IO

from project_video_hosting.celery import app
from video_hosting.services.user import VideoHostingService

@app.task
def process_video_task(input_file: IO, resolutions: list, file_name: str, video_id: int) -> None:
    service = VideoHostingService()
    service.process_video(input_file=input_file, resolutions=resolutions, file_name=file_name, video_id=video_id)
