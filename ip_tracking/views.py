from rest_framework import viewsets
from ip_tracking.models import RequestLog
from ip_tracking.serializers import RequestLogSerializer

class RequestLogViewSet(viewsets.ModelViewSet):
    queryset = RequestLog.objects.all()
    serializer_class = RequestLogSerializer
