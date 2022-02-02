from django.urls import path, include

urlpatterns = [
    path("api/v1/", include("apps.purchase.urls")),
    path("api/v1/", include("apps.user.urls")),
]
