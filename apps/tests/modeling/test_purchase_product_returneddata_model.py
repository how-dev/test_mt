from datetime import datetime
from django.test import TestCase

from apps.purchase.models import PurchaseModel, ProductsModel, ReturnedData
from apps.user.models import CustomerModel


class PurchaseProductReturnedDataModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_product = ProductsModel.objects.create(
            type="A",
            value="10.0",
            qty=10,
        )

        cls.base_purchase = PurchaseModel.objects.create(
            sold_at=datetime.now(),
            total="100.0",
            customer=CustomerModel.objects.create(
                name="Test",
                document="06872098112"
            )
        )
        cls.base_returned_data = ReturnedData.objects.create(
            raw_data=str({'createdAt': '2022-02-01T01:59:18.547Z', 'message': 'Cashback criado com sucesso!', 'id': '18', 'document': '62208311361', 'cashback': 150})
        )

    def test_product_model_has_information_fields(self):
        self.assertIsInstance(self.base_product.type, str)
        self.assertIsInstance(self.base_product.value, str)
        self.assertIsInstance(self.base_product.qty, int)
        self.assertIsInstance(self.base_product.is_active, bool)
        self.assertIsInstance(self.base_product.is_excluded, bool)

    def test_product_model_has_datetime_fields(self):
        self.assertIsInstance(self.base_product.creation_date, datetime)
        self.assertIsInstance(self.base_product.modification_date, datetime)

    def test_purchase_model_has_information_fields(self):
        self.assertIsInstance(self.base_purchase.total, str)

    def test_purchase_model_has_datetime_fields(self):
        self.assertIsInstance(self.base_purchase.sold_at, datetime)

    def test_purchase_model_has_related_fields(self):
        self.assertIsInstance(self.base_purchase.customer, CustomerModel)

    def test_returned_data_model_has_information_field(self):
        self.assertIsInstance(self.base_returned_data.raw_data, str)
