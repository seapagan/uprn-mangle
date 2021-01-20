# from django.urls import path

# from . import views

# urlpatterns = [
#     path("", views.index, name="index"),
# ]


from django.urls import include, path
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
# router.register(r"users", views.UserViewSet)
# router.register(r"groups", views.GroupViewSet)
router.register(r"addr", views.AddressBaseViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
]
