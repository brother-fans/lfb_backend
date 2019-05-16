from re import compile

from django.conf import settings

from core.mixins.response import ResponseMixin

LOGIN_EXEMPT_URLS = []

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    LOGIN_EXEMPT_URLS += [compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware(ResponseMixin):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        assert hasattr(request, 'user')

        path = request.path_info.lstrip('/')

        if not request.user.is_authenticated:
            if not any(m.match(path) for m in LOGIN_EXEMPT_URLS):
                self.success = False
                self.status = '10007'

                return self.get_json_response()

        request.session.set_expiry(3600)

        return self.get_response(request)
