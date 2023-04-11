from django.http.request import HttpRequest
from django.http.response import HttpResponse
from rest_framework_simplejwt.tokens import RefreshToken


def set_auth_token(request: HttpRequest, response: HttpResponse):
    user = request.user
    refresh = RefreshToken.for_user(user)

    refresh_token = str(refresh)
    access_token = str(refresh.access_token)

    response.set_cookie('refresh_token', refresh_token)
    response.set_cookie('access_token', access_token)
