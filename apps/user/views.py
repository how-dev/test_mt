from django.contrib.auth.hashers import check_password
from django.shortcuts import render
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from services.token_logic import ResetToken
from .models import UserModel
from .serializers import LoginSerializer, UserSerializer


class BaseLogin(APIView):
    messages = {
        "failure": {
            "data": {
                "status": status.HTTP_401_UNAUTHORIZED,
                "detail": "Some field is incorrect",
            },
            "status": status.HTTP_401_UNAUTHORIZED,
        },
        "success": {
            "data": {"status": status.HTTP_200_OK, "detail": None},
            "status": status.HTTP_200_OK,
        },
        "not_supported": {
            "data": {
                "status": status.HTTP_403_FORBIDDEN,
                "detail": "The param 'file_type' is not supported.",
            },
            "status": status.HTTP_403_FORBIDDEN,
        },
    }

    def success_result(self, result):
        message = self.messages["success"]
        message["data"]["result"] = result

        return message

    def post(self, request):
        data = request.data

        serializer = LoginSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        email = data["email"]
        password = data["password"]
        try:
            user = UserModel.objects.get(email=email)
        except UserModel.DoesNotExist:
            response = self.messages["failure"]
            return Response(**response)

        is_valid_password = check_password(password, user.password)

        if is_valid_password:
            user.last_login = timezone.now()
            user.save()
            data = UserSerializer(user).data

            token = Token.objects.get_or_create(user=user)[0]
            reset_token = ResetToken(token.key, user, 1)
            token = reset_token.reset_token()
            data["token"] = token.key

            response = self.success_result(data)
            return Response(**response)
        else:
            response = self.messages["failure"]
            return Response(**response)

