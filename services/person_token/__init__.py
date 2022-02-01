from rest_framework.authentication import TokenAuthentication


class TokenMaleta(TokenAuthentication):
    keyword = 'Bearer'
