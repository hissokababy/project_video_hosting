import hashlib
from typing import IO
from random import sample
from string import ascii_letters, digits

from django.core.files.storage import default_storage

from project_video_hosting.settings import VIDEO_RESOLUTIONS
from video_hosting.serializers import MyVideoSerializer
from video_hosting.models import User, Video
from video_hosting.exeptions import InvalidVideoId
from hosting_auth.services.user_auth import HostingAuth
from video_hosting.tasks import process_video_task


class VideoHostingService:
    def __init__(self):
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
                                     video=video_file)
        
        hasher = hashlib.sha256()
        with video.video.open('rb') as f:
            contents = f.read()
            hasher.update(contents)
    
            video_hash = hasher.hexdigest()

            try:
                existing_video = Video.objects.get(hash=video_hash)
                video.delete()
                return existing_video.pk
            
            except Video.DoesNotExist:
                video.hash = video_hash
                video.hls_dir_name = self.generate_dir_name(length=15)
                video.save()
            
                process_video_task.delay(input_file=video.video.name, resolutions=VIDEO_RESOLUTIONS, file_name=video.hls_dir_name,
                                         video_id=video.pk)
                

    def get_video(self, user_id: int, video_id: int) -> dict:
        try:
            video = Video.objects.get(created_by=user_id, pk=video_id, processed=True)

            serializer = MyVideoSerializer(video)
            return serializer.data
        except Video.DoesNotExist:
            raise InvalidVideoId

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
        symbols = ascii_letters + digits
        generated_dir = ''.join(sample(symbols, length))

        try:
            video = Video.objects.get(hls_dir_name=generated_dir)
            self.generate_dir_name(length=length)
        except Video.DoesNotExist:
            return generated_dir
        
   ###### ---->>>>>   РАБОТА С ВИДЕО   <<<<<---- ######


