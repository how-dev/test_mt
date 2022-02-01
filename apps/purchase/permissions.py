from django.contrib.auth.models import AnonymousUser
from rest_framework.permissions import BasePermission


class PurchasePermissions(BasePermission):
    protected_methods = ("GET", "PATCH", "PUT", "DELETE", "POST")
    intern_methods = protected_methods
    empresa_x_methods = ("POST",)
    empresa_y_methods = ()
    empresa_z_methods = ("POST",)

    def has_permission(self, request, _):
        method = request.method
        user = request.user

        if isinstance(user, AnonymousUser) and method in self.protected_methods:
            return False

        is_intern = user.user_type == "Interno MaisTODOS"
        is_empresa_x = user.user_type == "Empresa X"
        is_empresa_y = user.user_type == "Empresa Y"
        is_empresa_z = user.user_type == "Empresa Z"

        if is_intern and method in self.intern_methods:
            return True

        if is_empresa_x and method in self.empresa_x_methods:
            return True

        if is_empresa_y and method in self.empresa_y_methods:
            return True

        if is_empresa_z and method in self.empresa_z_methods:
            return True

        return False
