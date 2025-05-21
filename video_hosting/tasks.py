from typing import IO

from project_video_hosting.celery import app
from video_hosting.models import Video
from video_hosting.utils import VideoProcess

@app.task
def process_video_task(input_file: IO, resolutions: list, file_name: str, video_id: int) -> None:
    video_process = VideoProcess()

    master = video_process.create_hls(input_file=input_file, resolutions=resolutions, file_name=file_name)

    video = Video.objects.get(pk=video_id)

    video.master_playlist = master
    video.video.delete()
    video.processed = True
    video.save()
