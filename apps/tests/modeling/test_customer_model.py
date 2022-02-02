from django.test import TestCase

from apps.user.models import CustomerModel


class CustomerModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_customer = CustomerModel.objects.create(
            name="Test", document="06872098112"
        )

    def test_customer_model_has_information_fields(self):
        self.assertIsInstance(self.base_customer.name, str)
        self.assertIsInstance(self.base_customer.document, str)
