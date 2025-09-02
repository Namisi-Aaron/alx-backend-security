from django.db import models

class RequestLog(models.Model):
    ip_address = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    path = models.TextField()

    class Meta:
        ordering = ["-timestamp"]

class BlockedIP(models.Model):
    ip_address = models.GenericIPAddressField()
