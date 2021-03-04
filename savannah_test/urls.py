from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt import views as jwt_views

from customers.custom_token import CustomTokenView

from orders import views as order_views
from customers import views as customer_views

admin.site.site_header = "Savannah Sales Admin Panel"

router_admin = DefaultRouter()

router_admin.register(
    r"customers", customer_views.CustomerViewSet, basename="customers"
)

router_admin.register(r"items", order_views.ItemViewSet, basename="items")

router_admin.register(r"orders", order_views.OrderViewSet, basename="orders")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/admin/", include(router_admin.urls)),
    # for default login/logout and for the apis requiring authorization
    path("api/api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api/token/", CustomTokenView.as_view(), name="token_obtain_pair"),
    path(
        "api/refresh-token/", jwt_views.TokenRefreshView.as_view(), name="token_refresh"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)