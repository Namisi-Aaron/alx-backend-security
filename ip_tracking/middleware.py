from django.http import HttpResponseForbidden
from ip_tracking.models import RequestLog, BlockedIP

class RequestLoggingMiddleware:
    '''
    Middleware class that logs request details.
    Details: Logs the request method, IP address, and timestamp.
    '''
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the request and log its details.
        """
        try:

            ip = self.get_client_ip(request)
            geolocation = getattr(request, 'geolocation', None)

            if BlockedIP.objects.filter(ip_address=ip).exists():
                return HttpResponseForbidden("403 Forbidden")

            RequestLog.objects.create(
                ip_address=ip,
                path=request.path,
                method=request.method,
                city=getattr(geolocation, 'city', None),
                country=getattr(geolocation, 'country_name', None)
            )

            response = self.get_response(request)
            return response
        
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_client_ip(self, request):
        """
        Get the client's IP address from the request.
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
