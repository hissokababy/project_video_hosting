from pydantic import BaseModel

from video_hosting.exeptions import InvalidUserId


class UserMessage(BaseModel):
    id: int
    active: bool | None = True


class ValidateMessage:
        
    @classmethod
    def validate_user_id(cls, body: str) -> UserMessage:
        try:
            message = UserMessage.model_validate_json(body)
            return message
        except Exception as e:
            raise InvalidUserId(e)
