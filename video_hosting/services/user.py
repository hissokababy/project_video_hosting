from typing import IO

from django.core.files.storage import default_storage

from video_hosting.serializers import MyVideoSerializer
from video_hosting.models import User, Video
from video_hosting.exeptions import InvalidVideoId
from video_hosting.utils import VideoProcess
from hosting_auth.services.user_auth import HostingAuth

class VideoHostingService:
    def __init__(self):
        self.video_process = VideoProcess()
        self.hosting_auth = HostingAuth()

    def change_user(self, user_id: int, active: bool|None=True) -> None:
        user, created = User.objects.get_or_create(pk=user_id)

        if not created:
            user.is_active = active
            user.save()


    ###### ---->>>>>   РАБОТА С ВИДЕО   <<<<<---- ######
    def create_video(self, user_id: int, title: str, preview: IO, video_file: IO, duration: int) -> Video:

        user = self.hosting_auth.get_user(user_id=user_id)

        video = Video.objects.create(created_by=user, title=title, duration=duration, preview=preview, 
                                        hls_dir_name=self.generate_dir_name(length=15), video=video_file)
        video_hash = self.check_video_hash(video_file=video_file, video=video)

        return video

    def get_video(self, user_id: int, video_id: int) -> dict:
        try:
            video = Video.objects.get(created_by=user_id, pk=video_id, processed=True)

            serializer = MyVideoSerializer(video)
            return serializer.data
        except Video.DoesNotExist:
            raise InvalidVideoId
        
    
    def process_video(self, input_file: IO, resolutions: list, file_name: str, video_id: int):
        
        master = self.video_process.create_hls(input_file=input_file, resolutions=resolutions, file_name=file_name)

        video = Video.objects.get(pk=video_id)

        video.master_playlist = master
        video.video.delete()
        video.processed = True
        video.save()


    def delete_video(self, video_id: int, user_id: int):
        try:
            video = Video.objects.get(created_by=user_id, pk=video_id, processed=True)
        except Video.DoesNotExist:
            raise InvalidVideoId
        
        dir = video.hls_dir_name
        storage = default_storage
        storage.bucket.objects.filter(Prefix=dir).delete()
        video.delete()
    

    def generate_dir_name(self, length: int) -> str:
        generated = self.video_process.random_dir_name(length)
        video = Video.objects.filter(hls_dir_name=generated).exists()

        if video:
            self.generate_dir_name(length=length)
        else:
            return generated
        
    
    def check_video_hash(self, video_file: IO, video: Video) -> str:
        video_hash = self.video_process.create_video_hash(video_file=video_file)
        try:
            existing_video = Video.objects.get(hash=video_hash)
            print('est video s takim hash')
            video.hls_dir_name = existing_video.hls_dir_name
            video.master_playlist = existing_video.master_playlist
            # video.hash = existing_video.hash
            video.save()

        except Video.DoesNotExist:
            video.hash = video_hash
            video.save()
            return hash
        
   ###### ---->>>>>   РАБОТА С ВИДЕО   <<<<<---- ######


