from rest_framework.authentication import BaseAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth import get_user_model
from accounts.service import verify_token  # Sizning token tekshiruvchi funksiyangiz
from config.settings import SECRET_KEY  # SECRET_KEY ni settings dan olgan ma’qul

User = get_user_model()


class JWTAuthentication(BaseAuthentication):
    def authenticate(self, request):
        auth_header = request.headers.get('Authorization')

        if not auth_header:
            return None  # Token yo'q — boshqa authenticationlarga ruxsat beradi

        try:
            token_type, token = auth_header.split()
        except ValueError:
            raise AuthenticationFailed('Authorization header must be in the format: Bearer <token>')

        if token_type.lower() != 'bearer':
            raise AuthenticationFailed('Authorization header must start with Bearer')

        # Tokenni tekshirish
        payload = verify_token(token, SECRET_KEY, type='access')
        if not isinstance(payload, dict):
            raise AuthenticationFailed(payload)

        # Foydalanuvchini DB dan topish
        try:
            user = User.objects.get(id=payload['user_id'])
        except User.DoesNotExist:
            raise AuthenticationFailed('User not found')

        return (user, None)
