import hashlib
from django.conf import settings


def md5(data_string):
    # 使用settings.py里面的SELECT_KRY（系统每一次执行都随机生成一个）
    obj = hashlib.md5(settings.SECRET_KEY.encode('utf-8'))
    obj.update(data_string.encode('utf-8'))
    return obj.hexdigest()
