from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from apps.user.models import UserModel


class LoginTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.base_user = UserModel.objects.create(
            name="Test",
            email="test@email.com",
            password=make_password("test"),
            document="06872098112",
            user_type="Interno MaisTODOS",
        )

        cls.invalid_credentials = {
            "path": "/api/v1/login/",
            "data": {"email": "invalid@invalid.com", "password": "invalid"},
        }

        cls.invalid_password_and_valid_email = {
            "path": "/api/v1/login/",
            "data": {"email": "test@email.com", "password": "invalid"},
        }

        cls.valid_credentials = {
            "path": "/api/v1/login/",
            "data": {"email": "test@email.com", "password": "test"},
        }

    def test_cant_login_with_invalid_credentials(self):
        response = self.client.post(**self.invalid_credentials)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_login_with_invalid_password_and_valid_email(self):
        response = self.client.post(**self.invalid_password_and_valid_email)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_login_with_valid_credentials(self):
        response = self.client.post(**self.valid_credentials)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
