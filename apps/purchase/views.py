from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from services.purchase_validation import PurchaseValidation
from .models import PurchaseModel
from .serializers import PurchaseSerializer


class PurchaseViewSet(ModelViewSet):
    queryset = PurchaseModel.objects.all()
    serializer_class = PurchaseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        data = serializer.validated_data

        data = PurchaseValidation(data)

        errors = []

        if not data.is_valid_date():
            errors.append({"detail": "Invalid date to 'sold_at' field."})

        if not data.is_valid_total():
            errors.append({"detail": "Invalid value to 'total' field."})

        if not data.is_valid_document():
            errors.append({"detail": "Invalid value to 'document' field."})

        if len(errors) > 0:
            return Response(errors, status=status.HTTP_403_FORBIDDEN)

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
