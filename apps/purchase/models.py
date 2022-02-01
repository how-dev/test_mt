from django.db import models

from apps.user.models import CustomerModel


class ProductsModel(models.Model):
    type = models.CharField(
        max_length=255,
        choices=(
            ("A", "A"),
            ("B", "B")
        )
    )
    value = models.CharField(max_length=255)

    qty = models.IntegerField()

    is_active = models.BooleanField(default=True)
    is_excluded = models.BooleanField(default=False)

    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now_add=True)


class PurchaseModel(models.Model):
    sold_at = models.DateTimeField()

    total = models.CharField(max_length=255)

    products = models.ManyToManyField(ProductsModel)
    customer = models.ForeignKey(CustomerModel, on_delete=models.PROTECT)


class ReturnedData(models.Model):
    raw_data = models.CharField(max_length=255)
