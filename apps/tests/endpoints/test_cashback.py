from datetime import datetime

from django.contrib.auth.hashers import make_password
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from apps.purchase.models import ProductsModel, PurchaseModel
from apps.user.models import UserModel, CustomerModel


class CashbackTest(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.client = APIClient()

        cls.intern_token = {
            "HTTP_AUTHORIZATION": f'Bearer {Token.objects.create(user=UserModel.objects.create(name="Test", email="test1@email.com", password=make_password("test"), document="06872098112", user_type="Interno MaisTODOS"))}'
        }

        cls.empresa_x_token = {
            "HTTP_AUTHORIZATION": f'Bearer {Token.objects.create(user=UserModel.objects.create(name="Test", email="test2@email.com", password=make_password("test"), document="62208311361", user_type="Empresa X"))}'
        }

        cls.empresa_y_token = {
            "HTTP_AUTHORIZATION": f'Bearer {Token.objects.create(user=UserModel.objects.create(name="Test", email="test3@email.com", password=make_password("test"), document="90078144191", user_type="Empresa Y"))}'
        }

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

        cls.base_cashback = {
            "format": "json",
            "path": "/api/v1/cashback/",
            "data": {
                "sold_at": "2022-01-02 00:00:00",
                "customer": {
                   "document": "62208311361",
                   "name": "Howard"
                },
                "total": "21474836470.00",
                "products": [
                   {
                      "type": "C",
                      "value": "10.00",
                      "qty": 2147483647
                   }
                ]
            }
        }

        cls.base_200_cashback = {
            "format": "json",
            "path": "/api/v1/cashback/",
            "data": {
                "sold_at": "2022-01-02 00:00:00",
                "customer": {
                   "document": "62208311361",
                   "name": "Howard"
                },
                "total": "200.00",
                "products": [
                   {
                      "type": "C",
                      "value": "200.00",
                      "qty": 1
                   }
                ]
            }
        }

        cls.base_100_cashback = {
            "format": "json",
            "path": "/api/v1/cashback/",
            "data": {
                "sold_at": "2022-01-02 00:00:00",
                "customer": {
                   "document": "62208311361",
                   "name": "Howard"
                },
                "total": "100.00",
                "products": [
                   {
                      "type": "C",
                      "value": "100.00",
                      "qty": 1
                   }
                ]
            }
        }

        cls.base_50_cashback = {
            "format": "json",
            "path": "/api/v1/cashback/",
            "data": {
                "sold_at": "2022-01-02 00:00:00",
                "customer": {
                   "document": "62208311361",
                   "name": "Howard"
                },
                "total": "50.00",
                "products": [
                   {
                      "type": "C",
                      "value": "50.00",
                      "qty": 1
                   }
                ]
            }
        }

        cls.base_0_cashback = {
            "format": "json",
            "path": "/api/v1/cashback/",
            "data": {
                "sold_at": "2022-01-02 00:00:00",
                "customer": {
                   "document": "62208311361",
                   "name": "Howard"
                },
                "total": "25.00",
                "products": [
                   {
                      "type": "C",
                      "value": "25.00",
                      "qty": 1
                   }
                ]
            }
        }

        cls.retrieve_cashback = {
            "format": "json",
            "path": "/api/v1/cashback/1/",
            "data": {
                "sold_at": "2022-01-02 00:00:00",
                "customer": {
                   "document": "62208311361",
                   "name": "Howard"
                },
                "total": "21474836470.00",
                "products": [
                   {
                      "type": "C",
                      "value": "10.00",
                      "qty": 2147483647
                   }
                ]
            }
        }

        cls.invalid_total_cashback = {
            "format": "json",
            "path": "/api/v1/cashback/",
            "data": {
                "sold_at": "2022-01-02 00:00:00",
                "customer": {
                   "document": "62208311361",
                   "name": "Howard"
                },
                "total": "21836470.00",
                "products": [
                   {
                      "type": "C",
                      "value": "10.00",
                      "qty": 2147483647
                   }
                ]
            }
        }

        cls.invalid_date_cashback = {
            "format": "json",
            "path": "/api/v1/cashback/",
            "data": {
                "sold_at": "2200-01-02 00:00:00",
                "customer": {
                   "document": "62208311361",
                   "name": "Howard"
                },
                "total": "21474836470.00",
                "products": [
                   {
                      "type": "C",
                      "value": "10.00",
                      "qty": 2147483647
                   }
                ]
            }
        }

        cls.invalid_document_cashback = {
            "format": "json",
            "path": "/api/v1/cashback/",
            "data": {
                "sold_at": "2022-01-02 00:00:00",
                "customer": {
                   "document": "06872098111",
                   "name": "Howard"
                },
                "total": "21474836470.00",
                "products": [
                   {
                      "type": "C",
                      "value": "10.00",
                      "qty": 2147483647
                   }
                ]
            }
        }

        cls.invalid_body = {
            "format": "json",
            "path": "/api/v1/cashback/",
            "data": {
                "sold_at": "2022-01-02 00:00:00",
                "total": "21474836470.00",
                "products": [
                   {
                      "type": "C",
                      "value": "10.00",
                      "qty": 2147483647
                   }
                ]
            }
        }

    def test_cant_GET_cashbacks_unauthenticated(self):
        response = self.client.get(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_POST_cashbacks_unauthenticated(self):
        response = self.client.post(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_PATCH_cashbacks_unauthenticated(self):
        response = self.client.patch(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_PUT_cashbacks_unauthenticated(self):
        response = self.client.put(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_DELETE_cashbacks_unauthenticated(self):
        response = self.client.put(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_empresa_y_cant_POST_cashbacks(self):
        self.client.credentials(**self.empresa_y_token)
        response = self.client.post(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_empresa_y_cant_GET_cashbacks(self):
        self.client.credentials(**self.empresa_y_token)
        response = self.client.get(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_empresa_y_cant_PATCH_cashbacks(self):
        self.client.credentials(**self.empresa_y_token)
        response = self.client.patch(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_empresa_y_cant_PUT_cashbacks(self):
        self.client.credentials(**self.empresa_y_token)
        response = self.client.put(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_empresa_y_cant_DELETE_cashbacks(self):
        self.client.credentials(**self.empresa_y_token)
        response = self.client.delete(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_empresa_x_cant_GET_cashbacks(self):
        self.client.credentials(**self.empresa_x_token)
        response = self.client.get(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_empresa_x_cant_PATCH_cashbacks(self):
        self.client.credentials(**self.empresa_x_token)
        response = self.client.patch(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_empresa_x_cant_PUT_cashbacks(self):
        self.client.credentials(**self.empresa_x_token)
        response = self.client.put(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_empresa_x_cant_DELETE_cashbacks(self):
        self.client.credentials(**self.empresa_x_token)
        response = self.client.delete(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_POST_invalid_date_field_cashbacks(self):
        self.client.credentials(**self.intern_token)
        response = self.client.post(**self.invalid_date_cashback)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_POST_invalid_document_field_cashbacks(self):
        self.client.credentials(**self.intern_token)
        response = self.client.post(**self.invalid_document_cashback)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_POST_invalid_total_field_cashbacks(self):
        self.client.credentials(**self.intern_token)
        response = self.client.post(**self.invalid_total_cashback)

        self.assertEquals(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_cant_POST_invalid_body_cashbacks(self):
        self.client.credentials(**self.intern_token)
        response = self.client.post(**self.invalid_body)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_intern_can_POST_cashbacks(self):
        self.client.credentials(**self.intern_token)
        response = self.client.post(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_intern_can_GET_cashbacks(self):
        self.client.credentials(**self.intern_token)
        response = self.client.get(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_intern_can_GET_retrieve_cashbacks(self):
        self.client.credentials(**self.intern_token)
        response = self.client.get(**self.retrieve_cashback)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_intern_can_PATCH_cashbacks(self):
        self.client.credentials(**self.intern_token)
        response = self.client.patch(**self.retrieve_cashback)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_intern_cant_PUT_cashbacks(self):
        self.client.credentials(**self.intern_token)
        response = self.client.put(**self.retrieve_cashback)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_intern_cant_DELETE_cashbacks(self):
        self.client.credentials(**self.intern_token)
        response = self.client.delete(**self.retrieve_cashback)

        self.assertEquals(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_empresa_x_can_POST_cashbacks(self):
        self.client.credentials(**self.empresa_x_token)
        response = self.client.post(**self.base_cashback)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_15_percent_cashback(self):
        self.client.credentials(**self.intern_token)
        response = self.client.post(**self.base_200_cashback)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data["cashback"], 200 * 0.15)

    def test_10_percent_cashback(self):
        self.client.credentials(**self.intern_token)
        response = self.client.post(**self.base_100_cashback)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data["cashback"], 100 * 0.1)

    def test_5_percent_cashback(self):
        self.client.credentials(**self.intern_token)
        response = self.client.post(**self.base_50_cashback)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data["cashback"], 50 * 0.05)

    def test_0_percent_cashback(self):
        self.client.credentials(**self.intern_token)
        response = self.client.post(**self.base_0_cashback)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)
        self.assertEquals(response.data["cashback"], 0)
