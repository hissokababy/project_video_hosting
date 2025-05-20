from django.urls import path

from video_hosting.views import LoadVideoView, MyVideoView, DeleteMyVideoView

urlpatterns = [
    path('api/v1/load_video/', LoadVideoView.as_view()),
    path('api/v1/video/<int:pk>/', MyVideoView.as_view()),
    path('api/v1/delete_video/<int:pk>/', DeleteMyVideoView.as_view()),

]
