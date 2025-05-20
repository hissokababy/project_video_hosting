from hosting_auth.tokens import decode_access_token
from video_hosting.exeptions import InvalidUserId
from video_hosting.models import User


class HostingAuth:
    def __init__(self):
        pass

    ###### ---->>>>>   ВАЛИДАЦИЯ JWT ТОКЕНА ПОЛЬЗОВАТЕЛЯ  <<<<<---- ######
    def validate_access_token(self, access_token: str) -> User:
        decoded = decode_access_token(access_token)

        user = self.get_user(user_id=decoded['user_id'])
                
        return user
    

    def get_user(self, user_id: int) -> User:
        try:
            user = User.objects.get(pk=user_id)
            if user.is_active:
                return user
        except User.DoesNotExist:
            raise InvalidUserId('Invalid token')
    ###### ---->>>>>   ВАЛИДАЦИЯ JWT ТОКЕНА ПОЛЬЗОВАТЕЛЯ  <<<<<---- ######
