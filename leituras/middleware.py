from django.http import JsonResponse
from .models import Device

class DeviceApiKeyMiddleware:
    """
    Valida X-API-KEY em requests POST para /api/leituras/.
    Anexa o objecto Device em request.device se válido.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # valida apenas POST para /api/leituras
        path = request.path
        if path.startswith('/api/leituras') and request.method == 'POST':
            api_key = request.headers.get('X-API-KEY') or request.GET.get('api_key')
            if not api_key:
                return JsonResponse({'message':'API key required'}, status=401)
            try:
                device = Device.objects.get(api_key=api_key, active=True)
            except Device.DoesNotExist:
                return JsonResponse({'message':'Invalid API key'}, status=401)
            # anexa device ao request para usar no serializer/view
            request.device = device
        return self.get_response(request)
