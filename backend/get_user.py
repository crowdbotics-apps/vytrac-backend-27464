
from urllib.parse import parse_qs

from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
# from jwt import decode
from rest_framework_simplejwt.tokens import UntypedToken

from Functions.debuging import Debugging
from users.models import User


@database_sync_to_async
def get_user(querys):
    token = parse_qs(querys.decode("utf8"))['token'][0]
    token_data = UntypedToken(token)
    user_id = token_data["user_id"]
    try:
        return User.objects.get(id=user_id)
    except User.DoesNotExist:
        return AnonymousUser()
