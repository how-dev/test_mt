from django.test import TestCase

from services.document_logic import BrazilianDocumentLogics


class BrazilianDocumentLogicTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.object = BrazilianDocumentLogics
        cls.instance = BrazilianDocumentLogics()

    def test_can_validate_cpf(self):
        instance = self.instance
        instance.document = "06872098112"
        self.assertEquals(instance.is_valid_document(), True)

        instance.document = "06872098111"
        self.assertEquals(instance.is_valid_document(), False)

    def test_can_generate_valid_cpf(self):
        instance = self.instance
        instance.document = instance.force_valid_cpf()
        self.assertEquals(instance.is_valid_document(), True)
