from rest_framework import serializers


from .models import CustomerModel, UserModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            "id",
            "last_login",
            "email",
            "name",
            "document"
        )
        extra_kwargs = {
            "password": {"write_only": True},
            "is_active": {"write_only": True},
            "date_joined": {"write_only": True},
        }


class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomerModel
        fields = (
            "document",
            "name"
        )


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(required=True, write_only=True)

    def update(self, instance, validated_data):
        pass

    def create(self, validated_data):
        pass
