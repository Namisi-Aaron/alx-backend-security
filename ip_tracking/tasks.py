from celery import shared_task
from django.utils import timezone
from django.db.models import Q, Count
from ip_tracking.models import RequestLog, SuspiciousIP

FORBIDDEN_PATHS = [
    "/admin/", "/login/",
    "/etc/passwd", "/wp-login.php"
]


@shared_task
def anomaly_detection_task():
    now = timezone.now()
    last_1_hour = now - timezone.timedelta(hours=1)

    forbidden_q = Q()
    for path in FORBIDDEN_PATHS:
        forbidden_q |= Q(path__icontains=path)

    ips = (
        RequestLog.objects
        .filter(timestamp__gte=last_1_hour)
        .values_list("ip_address")
        .annotate(request_count=Count('id'))
    )

    for entry in ips:
        request_count = entry['request_count']
        ip = entry['ip_address']

        # Check rate limit
        if request_count > 100:
            mark_ip_as_suspicious(
                ip,
                f'High request rate detected: {request_count} requests in the last hour'
            )
            continue

        # Check for forbidden paths
        if RequestLog.objects.filter(ip_address=ip).filter(forbidden_q).exists():
            mark_ip_as_suspicious(ip, f'Attempted forbidden path(s)')


def mark_ip_as_suspicious(ip, reason):
    '''
    Creates or updates a SuspiciousIP record for the given IP address with the provided reason.
    Prevents duplicate entries for the same IP address.
    '''
    SuspiciousIP.objects.get_or_create(
        ip_address=ip,
        reason=reason
    )
