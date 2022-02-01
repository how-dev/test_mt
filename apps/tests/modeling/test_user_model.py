from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.test import TestCase

from apps.user.models import UserModel


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_user = UserModel.objects.create(
            name="Test",
            email="test@email.com",
            password=make_password("test"),
            document="06872098112",
            user_type="Interno MaisTODOS",
            last_login=datetime.now()
        )

    def test_user_model_hasnt_default_fields(self):
        self.assertIsInstance(self.base_user.username, type(None))
        self.assertIsInstance(self.base_user.user_permissions, type(None))
        self.assertIsInstance(self.base_user.first_name, type(None))
        self.assertIsInstance(self.base_user.last_name, type(None))
        self.assertIsInstance(self.base_user.groups, type(None))
        self.assertIsInstance(self.base_user.is_superuser, type(None))
        self.assertIsInstance(self.base_user.is_staff, type(None))

    def test_user_model_has_information_fields(self):
        self.assertIsInstance(self.base_user.name, str)
        self.assertIsInstance(self.base_user.email, str)
        self.assertIsInstance(self.base_user.password, str)
        self.assertIsInstance(self.base_user.is_active, bool)
        self.assertIsInstance(self.base_user.document, str)
        self.assertIsInstance(self.base_user.user_type, str)

    def test_user_model_has_datetime_fields(self):
        self.assertIsInstance(self.base_user.date_joined, datetime)
        self.assertIsInstance(self.base_user.last_login, datetime)

