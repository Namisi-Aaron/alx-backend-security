from rest_framework import viewsets
from ip_tracking.models import RequestLog
from ip_tracking.serializers import RequestLogSerializer
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit

@method_decorator(ratelimit(key='ip', rate='5/m', block=True), name='dispatch')
@method_decorator(ratelimit(key='user', rate='10/m', block=True), name='dispatch')
class RequestLogViewSet(viewsets.ModelViewSet):
    queryset = RequestLog.objects.all()
    serializer_class = RequestLogSerializer

@ratelimit(key='ip', rate='5/m', block=True)
@ratelimit(key='user', rate='10/m', block=True)
def login(request):
    pass
