from django.core.cache import cache
from django.utils import timezone


class UserActivityTimeMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        response = self.get_response(request)

        if request.user.is_authenticated:
            cache_key = f'user__{request.user.id}'
            cache.set(cache_key, timezone.now())

        return response
