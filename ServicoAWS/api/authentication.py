import jwt
from django.conf import settings
from rest_framework.exceptions import AuthenticationFailed

def decode_jwt(token):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        return payload
    except jwt.InvalidTokenError:
        raise AuthenticationFailed("Token inválido")

def get_user_id_from_request(request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise AuthenticationFailed("Token JWT ausente")

    token = auth_header.split(" ")[1]
    payload = decode_jwt(token)
    return payload['user_id']
