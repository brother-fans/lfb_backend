from django.views import View

from core.mixins.response import ResponseMixin

from ..models import User


class UserDetail(ResponseMixin, View):

    def post(self, request):
        username = request.user.username
        user = User.object_list.get_by_field(username=username)

        return self.get_json_response(user)