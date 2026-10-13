from django.conf import settings
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import AuthenticationFailed, TokenError
from rest_framework_simplejwt.tokens import RefreshToken

ACCESS_COOKIE = 'access_token'
REFRESH_COOKIE = 'refresh_token'


def _set_cookie(response, name, value, lifetime):
    response.set_cookie(
        name,
        value,
        max_age=int(lifetime.total_seconds()),
        httponly=True,              
        secure=not settings.DEBUG,  
        samesite='Lax',
    )


def set_access_cookie(response, access_token):
    _set_cookie(response, ACCESS_COOKIE, str(access_token), settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'])


def set_jwt_cookies(response, user):
    refresh = RefreshToken.for_user(user)
    set_access_cookie(response, refresh.access_token)
    _set_cookie(response, REFRESH_COOKIE, str(refresh), settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
    return response


def clear_jwt_cookies(response):
    response.delete_cookie(ACCESS_COOKIE)
    response.delete_cookie(REFRESH_COOKIE)
    return response


class JWTCookieAuthMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.jwt_auth = JWTAuthentication()

    def __call__(self, request):
        user = self._user_from_access(request.COOKIES.get(ACCESS_COOKIE))
        new_access = None
        if user is None:
            user, new_access = self._user_from_refresh(request.COOKIES.get(REFRESH_COOKIE))
        if user is not None:
            request.user = user

        response = self.get_response(request)
        if new_access is not None and ACCESS_COOKIE not in response.cookies:
            set_access_cookie(response, new_access)
        return response

    def _user_from_access(self, raw_token):
        if not raw_token:
            return None
        try:
            validated = self.jwt_auth.get_validated_token(raw_token)
            return self.jwt_auth.get_user(validated)
        except (AuthenticationFailed, TokenError):
            return None

    def _user_from_refresh(self, raw_token):
        if not raw_token:
            return None, None
        try:
            access = RefreshToken(raw_token).access_token
            return self.jwt_auth.get_user(access), str(access)
        except (AuthenticationFailed, TokenError):
            return None, None