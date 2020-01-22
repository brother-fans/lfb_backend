from datetime import datetime, timedelta

from dateutil.relativedelta import relativedelta
from django.forms.models import model_to_dict


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
            trim_string = datetime_input.split('T')[0]
            orig_date = datetime.strptime(trim_string, '%Y-%m-%d')

        end = orig_date + timedelta(days=days)

        return end.isoformat()

    @staticmethod
    def add_absolute_days(datetime_input, days=1):
        """增加绝对天数不切割时间

        Args:
            datetime_input (str, datetime): 基准日期时间
            days (int, optional): 要增加的天数. Defaults to 1.

        Returns:
            str
        """
        orig_date = datetime_input

        if isinstance(datetime_input, str):
            orig_date = datetime.strptime(datetime_input, '%Y-%m-%dT%H%M%S')

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

    @staticmethod
    def current_time_str() -> str:

        return datetime.now().isoformat()

    @staticmethod
    def days_between(earlier, later):
        """计算两个日期间的日子

        Args:
            earlier (str, datetime): 早一点的日期
            later (str, datetime): 晚一点的日期

        Returns:
            int: 两个日期之间的间隔天数
        """
        if isinstance(earlier, str):
            earlier = datetime.strptime(earlier, '%Y-%m-%dT%H%M%S')

        if isinstance(later, str):
            later = datetime.strptime(later, '%Y-%m-%dT%H%M%S')

        return (later - earlier).days

    @staticmethod
    def milli_timestamp():
        """以毫秒为单位返回当前时间搓

        Returns:
            int: 毫秒级时间戳
        """
        return datetime.now().microsecond

    @staticmethod
    def time_diff_in_ms(start, end):
        """计算毫秒级的时间差

        Args:
            start (str， datetime): 起始时间
            end (str， datetime): 结束时间

        Returns:
            int: 开始时间到结束时间的毫秒级时间差
        """
        if isinstance(start, str):
            start = datetime.strptime(start, '%Y-%m-%dT%H%M%S')

        if isinstance(end, str):
            end = datetime.strptime(end, '%Y-%m-%dT%H%M%S')

        return int((end - start).total_seconds() * 1000)

    @staticmethod
    def string_to_date(datetime_input, date_trans=True):
        """获取指定时间的日期

        Args:
            datetime_input (str, datetime): 需要转化的时间

        Returns:
            datetime: 转化后的日期
        """
        if isinstance(datetime_input, str):
            trim_string = datetime_input.split('T')[0]
            final_date = datetime.strptime(trim_string, '%Y-%m-%d')
        else:
            final_date = datetime_input

        return final_date.date() if date_trans is True else final_date

    @staticmethod
    def compare_date(estimate_input,
                     actual_input,
                     reverse=False,
                     boolean=False):
        """对日期进行比较

        Args:
            estimate_input (str, datetime): 预期时间
            actual_input (str, datetime): 实际时间
            reverse (bool, optional): 是否对比较时间进行反转. Defaults to False.
            boolean (bool, optional): 是否返回比较后的bool值. Defaults to False.

        Returns:
            str or bool: 比较后的最终时间或者比较后的bool值
        """
        estimate_date = DateTimeHelper.string_to_date(estimate_input)
        actual_date = DateTimeHelper.string_to_date(actual_input)
        if estimate_date > actual_date:
            if reverse is True:
                final_date = False if boolean else estimate_date.isoformat()
            else:
                final_date = True if boolean else actual_date.isoformat()
        else:
            if reverse is True:
                final_date = True if boolean else actual_date.isoformat()
            else:
                final_date = False if boolean else estimate_date.isoformat()

        return final_date

    @staticmethod
    def is_date_earlier(source_date, target_date=datetime.now()):
        """比较源日期是否早于目标日期

        Args:
            source_date (str, datetime): 源日期
            target_date (str, datetime): 目标比较日期. Defaults to 现在时间

        Returns:
            bool: 源日期是否早于目标日期
        """
        source_date = DateTimeHelper.string_to_date(source_date)
        target_date = DateTimeHelper.string_to_date(target_date)

        return source_date < target_date

    @staticmethod
    def is_date_equal(source_date, target_date=datetime.now()):
        """比较源日期是否和目标日期是同一天

        Args:
            source_date (str, datetime): 源日期
            target_date (str, datetime): 目标比较日期. Defaults to 现在时间

        Returns:
            bool: 源日期是否和目标日期是同一天
        """
        source_date = DateTimeHelper.string_to_date(source_date)
        target_date = DateTimeHelper.string_to_date(target_date)

        return source_date == target_date

    @staticmethod
    def trans_datetime_mfd(source_date, months=0, month_day=1, format=True):
        """获取指定月里的指定的某一天

        Args:
            datetime_input (string, datetime): 源日期
            months (int, optional): 月间隔(计算几个月之后). Defaults to 0.
            month_day (int, optional): 指定月的第几天. Defaults to 1.
            format (bool, optional): 是否进行iso8601格式转化. Defaults to True.

        Returns:
            str or datetime: 指定月里的某一天
        """
        input_date = DateTimeHelper.string_to_date(source_date,
                                                   date_trans=False)
        orig_date = input_date + relativedelta(months=months)
        first_day = datetime(orig_date.year, orig_date.month, month_day)

        return first_day.isoformat() if format is True else first_day

    @staticmethod
    def trans_datetime_wfd(source_date, weeks=0, weekdays=0, format=True):
        """获取指定周里的指定的某一天，默认周一

        Args:
            source_date (string, datetime): 源日期
            weeks (int, optional): 周间隔(计算几周之后). Defaults to 0.
            weekdays (int, optional): 指定周几，默认周一. Defaults to 0.
            format (bool, optional): 是否进行iso8601格式转化. Defaults to True.

        Returns:
            str or datetime: 指定周里的周几
        """
        input_date = DateTimeHelper.string_to_date(source_date,
                                                   date_trans=False)
        first_day = (input_date +
                     relativedelta(weeks=weeks,
                                   days=weekdays - input_date.weekday()))

        return first_day.isoformat() if format is True else first_day


class QuerySetHelper:

    @staticmethod
    def querydict_to_dict(querydict, fields=None):
        dict_obj = model_to_dict(querydict, fields)

        if hasattr(querydict, 'id'):
            dict_obj['id'] = querydict.id

        if ((not fields and hasattr(querydict, 'created')) or
                (fields and 'created' in fields)):
            dict_obj['created'] = querydict.created

        if ((not fields and hasattr(querydict, 'modified')) or
                (fields and 'modified' in fields)):
            dict_obj['modified'] = querydict.modified

        return dict_obj


class ListOperation:

    @staticmethod
    def intersect(a, b):
        """获取两个list的交集

        Args:
            a (list): list a
            b (list): list b

        Returns:
            list: a列表和b列表的交集
        """
        return list(set(a) & set(b))

    @staticmethod
    def union(a, b):
        """获取两个list的并集

        Args:
            a (list): list a
            b (list): list b

        Returns:
            list: a列表和b列表的并集
        """
        return list(set(a) | set(b))

    @staticmethod
    def orderly_unique(a):
        """对一个列表有序去重

        Args:
            a (list): list a

        Returns:
            list: 有序去重后的列表
        """
        unique_list = list(set(a))
        unique_list.sort(key=a.index)

        return unique_list
