from django.views import View

from core.mixins.response import ResponseMixin
from core.utils import Validators

from ..models import User


class UserDetail(ResponseMixin, View):

    def post(self, request):

        username = request.user.username
        user = User.object_list.get_by_field(username=username)

        return self.get_json_response(user)


class UserCreation(ResponseMixin, View):



    def post(self, request):

        args = request.POST.copy()

        if args:

            validator = Validators(request_body=args)
            username = validator.args_validator(
                arg_key='username',
                null=False,
                valid_type=str)

