from rest_framework.viewsets import ModelViewSet

from .models import PurchaseModel


class PurchaseViewSet(ModelViewSet):
    queryset = PurchaseModel.objects.all()

