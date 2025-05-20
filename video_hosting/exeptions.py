from rest_framework.exceptions import APIException
from rest_framework import status

class InvalidUserId(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = ('invalid id')
    default_code = 'invalid_user_id'

class InvalidVideoId(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = ('Invalid video id or video is in process')
    default_code = 'invalid_video_id'


class InvalidTokenExeption(APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = ('Invalid token')
    default_code = 'invalid_token'

