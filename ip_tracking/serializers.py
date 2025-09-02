from rest_framework import serializers
from ip_tracking.models import RequestLog


class RequestLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = RequestLog
        fields = ['ip_address', 'timestamp', 'path']
