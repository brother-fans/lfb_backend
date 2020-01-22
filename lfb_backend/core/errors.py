from requests.exceptions import RequestException


class OperationalError(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = f'【用户操作错误】{message}'

    def __str__(self):
        return self.message


class DataError(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = f'【用户/系统数据错误】{message}'

    def __str__(self):
        return self.message


class RedisError(Exception):

    def __init__(self, message):
        super().__init__(message)
        self.message = f'【redis错误】{message}'

    def __str__(self):
        return self.message


class ExternalError(RequestException):

    def __init__(self, message):
        super().__init__(message)
        self.message = f'【request请求错误】{message}'

    def __str__(self):
        return self.message
