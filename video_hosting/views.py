from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from video_hosting.serializers import LoadVideoSerializer
from video_hosting.services.user import VideoHostingService

# Create your views here.


class LoadVideoView(APIView):
    service = VideoHostingService()

    def post(self, request):
        serializer = LoadVideoSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)

        video = self.service.create_video(user_id=request.user.pk, title=serializer.validated_data.get('title'),
                                        duration=serializer.validated_data.get('duration'),
                                        preview=serializer.validated_data.get('preview'), 
                                        video_file=serializer.validated_data.get('video'))

        return Response(video, status=status.HTTP_202_ACCEPTED)
    

class MyVideoView(APIView):
    service = VideoHostingService()

    def get(self, request, pk):

        video = self.service.get_video(user_id=self.request.user.pk, video_id=pk)
        return Response(video, status=status.HTTP_202_ACCEPTED)
            

class DeleteMyVideoView(APIView):
    service = VideoHostingService()

    def delete(self, request, pk):

        video = self.service.delete_video(user_id=self.request.user.pk, video_id=pk)
        return Response(video, status=status.HTTP_200_OK)

