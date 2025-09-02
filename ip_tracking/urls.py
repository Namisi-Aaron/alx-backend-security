from django.urls import path, include
from rest_framework import routers
from ip_tracking.views import RequestLogViewSet

router = routers.DefaultRouter()
router.register(r'request-logs', RequestLogViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
