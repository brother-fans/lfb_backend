from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ImproperlyConfigured
from django.views import View

from core.mixins.response import ResponseMixin
from core.utils import Validators


class Login(ResponseMixin, View):

    def post(self, request):

        args = request.POST.copy()

        if args:
            validator = Validators(request_body=args)
            username = validator.args_validator(
                arg_key='username',
                valid_type=str,
                null=False)
            password = validator.args_validator(
                arg_key='password',
                valid_type=str,
                null=False)

            is_valid_request, validation_msg = validator.is_valid_request()
            if is_valid_request:
                user = None
                try:
                    user = authenticate(request,
                                        username=username,
                                        password=password)
                except ImproperlyConfigured:
                    pass

                if user is not None:
                    request.session['username'] = username
                    request.session.set_expiry(1200)
                    login(request, user)
                else:
                    self.success = False
                    self.status = '10003'
            else:
                self.success = False
                self.status = '10002'
                self.msg = validation_msg
        else:
            self.success = False
            self.status = '10001'

        return self.get_json_response()


class Logout(ResponseMixin, View):

    def post(self, request):
        logout(request)
        return self.get_json_response()
