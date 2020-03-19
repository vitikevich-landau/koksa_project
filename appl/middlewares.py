from django.utils.deprecation import MiddlewareMixin
from threading import local

_locals = local()


class CurrentHostMiddleware(MiddlewareMixin):
    def process_request(self, request):
        _locals.host_name_ = request.get_host()


def get_current_host():
    return _locals.host_name_
