import json

from core.helpers import DataTypeHelper


class Validators:

    SPACIAL_HANDLING = ['json', 'list', 'dict']

    def __init__(self, request_body=None):
        self.request_body = request_body
        self.validations = []
        self.msgs = []
        self.msg = ''

    def args_validator(self,
                       arg_key,
                       default=None,
                       valid_type=None,
                       null=True,
                       choices=None,
                       verbose_note=''):
        """http请求参数校验

        Args:
            arg_key (str): 参数名
            default (any, optional): Defaults to None. 默认值
            valid_type (class, optional): Defaults to None. 参数类型
            null (bool, optional): Defaults to True. 是否允许空值
            choices (list, optional): Defaults to None. 是否有限选项
            verbose_note (str): Defaults to ''. 参数说明

        Returns:
            any: 参数取值
            bool: 是否有效
            str: 验证信息

        """

        valid = True
        msg = '参数%s' % arg_key
        arg_value = self.request_body.get(arg_key)

        if (not arg_key or not arg_key) and not null:
            valid = False
            msg += '缺失'

        if valid_type:
            if valid_type in self.SPACIAL_HANDLING and arg_value:
                arg_value = json.loads(arg_value)
            elif valid_type is bool and arg_value:
                arg_value = DataTypeHelper.str_to_bool(arg_value)
            elif arg_value:
                try:
                    arg_value = valid_type(arg_value)
                except ValueError:
                    valid = False
                    msg += '类型错误'

        if arg_value and choices and arg_value not in choices:
            valid = False
            msg += '取值错误'

        if (arg_value is None or arg_value == '') and default is not None:
            arg_value = default

        self.validations.append(valid)
        self.msgs.append(msg)

        return arg_value

    def is_valid_request(self):
        try:
            false_validation_position = self.validations.index(False)
            return False, self.msgs[false_validation_position]
        except ValueError:
            return True, ''
