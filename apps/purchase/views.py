from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from services.person_token import BearerToken
from services.purchase_validation import PurchaseValidation
from .models import PurchaseModel, ReturnedData
from .permissions import PurchasePermissions
from .serializers import PurchaseSerializer


class PurchaseViewSet(ModelViewSet):
    queryset = PurchaseModel.objects.all()
    serializer_class = PurchaseSerializer
    authentication_classes = [BearerToken]
    permission_classes = [PurchasePermissions]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data
        data = PurchaseValidation(data)

        if data.has_error:
            return Response(data.errors, status=status.HTTP_403_FORBIDDEN)

        self.perform_create(serializer)

        cashback = data.send_cashback()
        ReturnedData.objects.create(raw_data=str(cashback))
        return Response(cashback, status=status.HTTP_201_CREATED)

    @method_decorator(cache_page(60, key_prefix="list"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
