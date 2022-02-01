from rest_framework.serializers import ModelSerializer

from .models import PurchaseModel, ProductsModel
from apps.user.models import CustomerModel
from apps.user.serializers import CustomerSerializer


class ProductsSerializer(ModelSerializer):
    class Meta:
        model = ProductsModel
        fields = (
            "type",
            "value",
            "qty"
        )


class PurchaseSerializer(ModelSerializer):
    customer = CustomerSerializer()
    products = ProductsSerializer(many=True)

    class Meta:
        model = PurchaseModel
        fields = (
            "sold_at",
            "customer",
            "total",
            "products"
        )

        extra_kwargs = {
            "sold_at": {
                "required": True
            },
            "customer": {
                "required": True
            },
            "total": {
                "required": True
            },
            "products": {
                "required": True
            }
        }

    def create(self, validated_data):
        customer = validated_data["customer"]
        customer = CustomerModel.objects.create(**customer)
        validated_data["customer"] = customer

        products = validated_data.pop("products")
        products_list = []
        for product in products:
            products_list.append(ProductsModel.objects.create(**product).id)

        purchase = PurchaseModel.objects.create(**validated_data)
        purchase.products.add(*products_list)

        return purchase
