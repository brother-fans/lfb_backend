from datetime import datetime, timedelta


class DataTypeHelper:

    @staticmethod
    def str_to_bool(bool_str):
        if (bool_str == 'true'
            or bool_str == 'True'
                or bool_str == '1'):
            return True

        return False


class DateTimeHelper:
    """日期/时间类型数据工具
    """

    @staticmethod
    def convert_timestamp_to_datetime(timestamp):
        """时间戳类型转换

        Args:
            timestamp (int): unix timestamp

        Returns:
            str: iso8601 string, e.g. 2019-02-23T00:23:29+01:00
        """

        return datetime.fromtimestamp(timestamp).isoformat()

    @staticmethod
    def convert_datetime_to_str(datetime_obj):
        """转换datetime对象为iso8601字符串

        Args:
            datetime_obj (datetime): 日期时间对象

        Returns:
            str: iso8601 string
        """

        return datetime_obj.isoformat() if datetime_obj else None

    @staticmethod
    def add_days(datetime_input, days=1):
        """增加日子

        Args:
            datetime_input (str|datetime obj): 基准日期时间
            days (int, optional): Defaults to 1. 要增加的天数

        Returns:
            str: 增加后的日期时间字符串
        """

        orig_date = datetime_input

        if isinstance(datetime_input, str):
            trimed = datetime_input.split('T')[0]
            orig_date = datetime.strptime(trimed, '%Y-%m-%d')

        end = orig_date + timedelta(days=days)

        return end.isoformat()

    @staticmethod
    def trim_date_string(date_string):
        """切割iso8601 string

        Args:
            date_string (str): iso8601 格式的时间日期字符串

        Returns:
            str: 切割后的日期字符串
        """

        return date_string.split('T')[0]
