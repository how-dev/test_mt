from django.urls import path

from .views import PurchaseViewSet

urlpatterns = [
    path("cashback/", PurchaseViewSet.as_view({"post": "create"})),
]
