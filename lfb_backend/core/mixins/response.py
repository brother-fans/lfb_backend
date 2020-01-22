"""通用Http Response处理模块
"""
from any_case import converts_keys
from django.http import HttpResponse, JsonResponse


class ResponseMixin:

    STATUS_MSG = {
        '00000': '成功',
        '10000': '系统错误',
        '10001': '参数缺失',
        '10002': '参数有误',
        '10003': '用户名或密码错误',
        '10004': '用户无此权限',
        '10005': '记录已存在',
        '10006': '找不到记录',
        '10007': '请先登录',
        '10008': '非法操作'
    }

    def __init__(self):
        self._status = '00000'
        self._success = True
        self._msg = self.STATUS_MSG.get(self._status)

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, value):
        self._status = value
        self.msg = self.STATUS_MSG.get(value)

    @property
    def success(self):
        return self._success

    @success.setter
    def success(self, value):
        self._success = value

    @property
    def msg(self):
        return self.msg

    @msg.setter
    def msg(self, value):
        self._msg = value

    def get_json_response(self, *args, **kwargs):
        """获取对应信息的JSON Response
        """

        kwargs['success'] = self.success
        kwargs['status'] = self.status
        kwargs['msg'] = self.msg
        kwargs['data'] = (None
                          if not args
                          else converts_keys(args[0], case='camel'))

        return JsonResponse(kwargs)

    def get_download_response(self, file_name, file_type):
        """获取csv Response

        Args:
            file_name (str): 文件名
            file_type (object, optional): 文件类型
        """
        resp = HttpResponse(content_type='text/csv')
        resp['Content-Disposition'] = ('attachment; filename="{}.{}"'
                                       .format(file_name, file_type))
        resp.write(u'\ufeff'.encode('utf8'))
        return resp
