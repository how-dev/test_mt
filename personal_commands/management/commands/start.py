from django.contrib.auth.hashers import make_password
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

from apps.user.models import UserModel
from services.document_logic import BrazilianDocumentLogics


class Command(BaseCommand, BrazilianDocumentLogics):
    def handle(self, *_, **options):
        if len(UserModel.objects.all()) < 3:
            test1 = UserModel.objects.create(
                name="Howard",
                email="test1@mail.com",
                document=self.force_valid_cpf(),
                password=make_password("test"),
                user_type="Interno MaisTODOS",
            )

            Token.objects.get_or_create(user=test1)

            test2 = UserModel.objects.create(
                name="Howard",
                email="test2@mail.com",
                document=self.force_valid_cpf(),
                password=make_password("test"),
                user_type="Empresa X",
            )

            Token.objects.get_or_create(user=test2)

            test3 = UserModel.objects.create(
                name="Howard",
                email="test3@mail.com",
                document=self.force_valid_cpf(),
                password=make_password("test"),
                user_type="Empresa Y",
            )

            Token.objects.get_or_create(user=test3)
