from django.db import models

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=10, blank=True, null=True)
    path = models.TextField()
    city = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        ordering = ["-timestamp"]

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField()

class SuspiciousIP(models.Model):
    ip_address = models.GenericIPAddressField()
    reason = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
