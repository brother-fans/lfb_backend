from datetime import datetime

from django.db.models import QuerySet

from core.helpers import DateTimeHelper


class DateTimeQuerySet(QuerySet):

    def range(self,
              datetime_field_name,
              start=None,
              end=None,
              days=1.5,
              is_deleted=False):
        """获取日期时间区间数据

        Args:
            datetime_field_name （str): 日期时间字段名
            start （datetime/str, optional): Defaults to None. 起始时间
            end （datetime/str, optional): Defaults to None. 起始时间
            days (float): 间隔天数. Defaults to 1.5.
            is_deleted （bool, optional): Defaults to False. 是否查询已删除数据

        Returns:
            queryset: 符合日期时间筛选区间的数据
        """

        query = {}

        if is_deleted is not None:
            query['is_deleted'] = is_deleted

        if start and end:
            start = DateTimeHelper.trim_date_string(start)
            end = DateTimeHelper.add_days(end, days)
            query_key = datetime_field_name + '__range'
            query[query_key] = [start, end]

        if not start and end:
            end = DateTimeHelper.add_days(end)
            query_key = datetime_field_name + '__lt'
            query[query_key] = end

        if start and not end:
            query_key = datetime_field_name + '__gte'
            query[query_key] = start

        return self.filter(**query)


class DisplayQuerySet(QuerySet):

    def values(self, *fields, **expressions):
        fields_list = self.model.DISPLAY_FIELDS
        fields_list += fields

        if (expressions.get('use_field_only', False) is False and
                hasattr(self.model, 'DISPLAY_FIELDS') is True):
            fields_list += self.model.DISPLAY_FIELDS

        if expressions.get('use_field_only') is not None:
            expressions.pop('use_field_only')

        return super().values(*fields_list, **expressions)

    def values_list(self,
                    *fields,
                    flat=False,
                    named=False,
                    use_fields_only=False):
        fields_list = fields

        if (use_fields_only is False and
                hasattr(self.model, 'DISPLAY_FIELDS') is True):
            fields_list += self.model.DISPLAY_FIELDS

        return super().values_list(*fields_list, flat=flat, named=named)


class CRUDQuerySet(QuerySet):

    def create_with_name_check(self, **kwargs):
        """创建时校验数据库中是否存在同名记录
        """
        name = kwargs.get('name')
        if not self.filter(name=name).exists():

            return super().create(**kwargs)

    def create_with_field_check(self, field_query, **kwargs):
        """创建时根据传入字段校验数据库中是否存在记录

        Args:
            field_query (dict): 需要校验的字段
        """
        if not self.filter(**field_query).exists():

            return super().create(**kwargs)

    def update_by_id(self, id, **kwargs):
        """更新数据

        Args:
            id (int): model对象id

        Returns:
            model obj: 更新后的model数据对象
        """

        found = self.filter(id=id)

        if found:

            if (kwargs.get('is_deleted')
                    and hasattr(self.model, 'RENAME_FIELD')
                    and self.model.RENAME_FIELD is not None):

                kwargs[self.model.RENAME_FIELD] = (
                    '{}_deleted_{}'
                    .format(getattr(found[0], self.model.RENAME_FIELD), id))

            if (kwargs.get('modified') is None
                    and hasattr(self.model, 'modified')):

                kwargs['modified'] = datetime.now().isoformat()

            found.update(**kwargs)

            return found[0]

    def get_by_id(self, id, fields=()):
        """通过id获取json serializable对象

        Args:
            id (int): model object id
            fields (tuple, optional): Defaults to (). 除了默认字段之外需要额外获取的字段

        Returns:
            dict: model对象详情(json serializable)
        """

        found = self.filter(id=id)
        if found:
            return found.values(*fields)[0]
        return {}

    def get_by_field(self, field_query, fields=()):
        """通过字段获取son serializable对象

        Args:
            field_query (dict): model object fields
            fields (tuple, optional): Defaults to (). 除了默认字段之外需要额外获取的字段

        Returns:
            dict: model对象详情(json serializable)
        """
        found = self.filter(**field_query)
        if found:
            return self.values(*fields)[0]
        return {}

    def update_with_field_check(self, field_query, id, **kwargs):
        """更新时根据传入字段校验数据库中是否存在记录

        Args:
            field_query (dict): 需要校验的字段
            id ([type]): 更新表主键id

        Returns:
            QuerySet
        """
        found = self.filter(**field_query)
        if not found:
            found = self.filter(id=id)
            found.update(**kwargs)
        elif found[0].id == id:
            found.update(**kwargs)

        return found


class FilterQuerySet(QuerySet):

    def existed(self, **kwargs):
        if hasattr(self.model, 'is_deleted'):
            kwargs['is_deleted'] = False

        return super().filter(**kwargs)

    def order_by_field(self, field_name, order):
        order = '-%s' % field_name if order == -1 else field_name

        return super().order_by(order)

    def fuzzy_filter(self, field_name, search_string, split=' '):
        """对指定字段field_name进行模糊查询

        Args:
            field_name (str): 查询字段名称
            search_string (str): 模糊查询字符串
            split (str, optional): 查询字符串切割符. Defaults to ' '.
        """
        string_list = search_string.split(split)
        query_key = f'{field_name}_icontains'
        for string in string_list:
            if string:
                query = {query_key: string}
                self = self.filter(**query)

        return self
