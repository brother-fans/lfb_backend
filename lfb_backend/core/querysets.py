from datetime import datetime

from django.db.models import QuerySet

from core.helpers import DateTimeHelper


class DateTimeQuerySet(QuerySet):

    def range(self,
              datetime_field_name,
              start=None,
              end=None,
              is_deleted=False):
        """获取日期时间区间数据

        Args:
            datetime_field_name （str): 日期时间字段名
            start （datetime/str, optional): Defaults to None. 起始时间
            end （datetime/str, optional): Defaults to None. 起始时间
            is_deleted （bool, optional): Defaults to False. 是否查询已删除数据

        Returns:
            queryset: 符合日期时间筛选区间的数据
        """

        query = {'is_deleted': is_deleted}

        if start and end:
            start = DateTimeHelper.trim_date_string(start)
            end = DateTimeHelper.add_days(end)
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

        if expressions.get('use_field_only') is True:
            fields_list = fields
            expressions.pop('use_field_only')

        return super().values(*fields_list, **expressions)

    def values_list(self,
                    *fields,
                    flat=False,
                    named=False,
                    use_fields_only=False):

        fields_list = self.model.DISPLAY_FIELDS
        fields_list += fields

        if use_fields_only:
            fields_list = fields

        return super().values_list(*fields_list, flat=flat, named=named)


class CRUDQuerySet(QuerySet):

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


class FilterQuerySet(QuerySet):

    def existed(self, **kwargs):
        if hasattr(self.model, 'is_deleted'):
            kwargs['is_deleted'] = False

        return super().filter(**kwargs)

    def order_by_field(self, field_name, order):
        order = '-%s' % field_name if order == -1 else field_name

        return super().order_by(order)
