import os
from uuid import uuid1


def upload_rank_photo(instance, filename: str)->str:
    ext = filename.split('.')[-1]
    return os.path.join('ranks', f'{instance.rank_name}.{ext}')

def upload_user_photo(instance, filename: str)->str:
    ext = filename.split('.')[-1]
    return os.path.join('avatars', f'{uuid1()}.{ext}')