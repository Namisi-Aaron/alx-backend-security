from ip_tracking.models import BlockedIP

def add_blocked_ip(ip_address):
    """
    Adds an IP address to the blocked list.
    """
    BlockedIP.objects.get_or_create(ip_address=ip_address)
