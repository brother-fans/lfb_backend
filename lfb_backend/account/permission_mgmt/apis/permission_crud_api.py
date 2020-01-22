from django.views import View

from core.helpers import QuerySetHelper
from core.mixins.response import ResponseMixin
from core.utils import Validators

from ..models import Role, Permission


class RoleCreation(ResponseMixin, View):
    """角色创建视图
    """

    def post(self, request):

        args = request.POST.copy()

        if args:
            validator = Validators(request_body=args)
            role_name = validator.args_validator(
                arg_key='roleName',
                valid_type=str,
                null=False,
                verbose_note='角色名称')

            username = request.user.username
            is_valid_request, validation_msg = validator.is_valid_request()
            if is_valid_request:
                field_query = {
                    'name': role_name,
                    'is_deleted': False
                }
                role = (Role
                        .object_list
                        .create_with_field_check(field_query,
                                                 name=role_name,
                                                 modifier=username,
                                                 operator=username))
                if role:
                    default_per_ids = list(Permission
                                           .objects
                                           .filter(is_private=False,
                                                   is_deleted=False)
                                           .values('id', flat=True))
                    role.permission.add(*default_per_ids)
                    data = (QuerySetHelper
                            .querydict_to_dict(role,
                                               Role.DISPLAY_FIELDS))

                    return self.get_json_response(data)

            else:
                self.success = False
                self.status = '10002'
                self.msg = validation_msg
        else:
            self.success = False
            self.status = '10001'

        return self.get_json_response()
