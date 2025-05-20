import jwt

from video_hosting.exeptions import InvalidTokenExeption
from project_video_hosting.settings import (ALGORITHMS, 
                                  ACCESS_TOKEN_SECRET_KEY, 
                                  HS256_ALGORITHM, RS256_ALGORITHM, ACCESS_PUBLIC_KEY)

def decode_access_token(access_token: str) -> dict:
    try:
        if ALGORITHMS == HS256_ALGORITHM:
            decoded = jwt.decode(access_token, ACCESS_TOKEN_SECRET_KEY, algorithms=ALGORITHMS)
        elif ALGORITHMS == RS256_ALGORITHM:
            decoded = jwt.decode(access_token, str(ACCESS_PUBLIC_KEY), algorithms=ALGORITHMS)

        return decoded
    except:
        raise InvalidTokenExeption('Invalid token')