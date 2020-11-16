from rest_framework.throttling import SimpleRateThrottle


class UserThrottle(SimpleRateThrottle):
    scope = 'user'

    def get_cache_key(self, request, view):
        return request.user

