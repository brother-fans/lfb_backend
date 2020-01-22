import json
import threading
import traceback
from json import JSONDecodeError

import redis
import requests
from django.conf import settings

from elasticsearch import Elasticsearch
from log.log import lx_log

from .constants import (DEFAULT_HEADERS, DOC_TYPE, REDIS_ENCODING,
                        REDIS_MAX_CONN)
from .errors import ExternalError
from .helpers import DataTypeHelper


class Validators:

    SPECIAL_HANDLING = ['json', 'list', 'dict']
    SPECIAL_TYPE = [list, dict]

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
                       verbose_note='',
                       is_multi=False):
        """http请求参数校验

        Args:
            arg_key (str): 参数名
            default (any, optional): Defaults to None. 默认值
            valid_type (class, optional): Defaults to None. 参数类型
            null (bool, optional): Defaults to True. 是否允许空值
            choices (list, optional): Defaults to None. 是否有限选项
            verbose_note (str): Defaults to ''. 参数说明
            is_multi (bool): 是否是多类型参数

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
            if valid_type in self.SPECIAL_HANDLING and arg_value:
                try:
                    arg_value = json.loads(arg_value)
                except JSONDecodeError as e:
                    info = str(traceback.format_exc()).replace('\n', '    ')
                    lx_log.debug(f'【json参数验证错误】：{info}')
                    traceback.print_tb(e.__traceback__)
                    valid = False
                    msg += '类型错误'
                if type(arg_value) not in self.SPECIAL_TYPE:
                    valid = False
                    msg += '类型错误'
            elif valid_type is bool and arg_value:
                arg_value = DataTypeHelper.str_to_bool(arg_value)
            elif (arg_value is not None and arg_value != ''
                    and arg_value != 'None' and arg_value != 'null'):
                try:
                    arg_value = valid_type(arg_value)
                except ValueError:
                    valid = False
                    msg += '类型错误'

        if arg_value and choices and arg_value not in choices:
            valid = False
            msg += '取值错误'

        if ((arg_value is None or arg_value == ''
             or arg_value == 'None' or arg_value == 'null')
                and default is not None):
            arg_value = default

        if arg_value == 'None' or arg_value == 'null':
            arg_value = None

        if is_multi is False:
            self.validations.append(valid)
            self.msgs.append(msg)
        else:

            return valid, arg_value

        return arg_value

    def is_valid_request(self):
        try:
            false_validation_position = self.validations.index(False)

            return False, self.msgs[false_validation_position]
        except ValueError:

            return True, ''

    def multi_type_args(self,
                        arg_key,
                        default=None,
                        valid_types=[],
                        null=True,
                        choices=None,
                        verbose_note=''):
        """http请求多类型参数校验

        Args:
            arg_key (str): 参数名
            default (any, optional): Defaults to None. 默认值
            valid_types (list, optional): Defaults to []. 参数类型列表
            null (bool, optional): Defaults to True. 是否允许空值
            choices (list, optional): Defaults to None. 是否有限选项
            verbose_note (str): Defaults to ''. 参数说明

        Returns:
            any: 参数取值
            bool: 是否有效
            str: 验证信息

        """
        valids = []
        arg_value = None
        for valid_type in valid_types:
            valid, value = self.args_validator(arg_key,
                                               default=default,
                                               valid_type=valid_type,
                                               null=null,
                                               choices=choices,
                                               verbose_note=verbose_note,
                                               is_multi=True)
            if valid is True:
                arg_value = value
                valids.append(valid)

        if any(valid) is False:
            self.validations.append(False)
            self.msgs.append(f'参数{arg_key}参数取值类型不在{valid_types}范围')

        return arg_value

    @staticmethod
    def check_list_ele_type(list_ele, data_type):
        """检查列表内子元素类型是否符合要求

        Args:
            list_ele (list): 列表参数
            data_type (object, optional): 列表参数子元素类型

        Returns:
            bool
        """

        return all([isinstance(ele, data_type) for ele in list_ele])


class ESUtil:
    """elastic search相关操作
    """

    def __init__(self):
        self.es_host = settings.ES_OPTIONS.get('HOST')
        self.es_port = settings.ES_OPTIONS.get('PORT')
        self.es = Elasticsearch(settings.ES_OPTIONS.get('NODE'),
                                sniff_on_connection_fail=True)
        self.indexes_search_url = (f'http://{self.es_host}:{self.es_port}/'
                                   f'_cat/indices?v')
        self.alias_url = f'http://{self.es_host}:{self.es_port}/_alias'

    def es_search(self, index, dsl):
        """查询es数据

        Args:
            index (str): 需要查询的索引
            dsl (str): 查询dsl语句json

        Returns:
            str: 查询结果json
        """
        info = self.es.search(index=index, body=dsl)

        return info

    def bulk_es_insert(self, data, index, doc_type=DOC_TYPE):
        """es批量往索引里插入数据

        Args:
            data (str): 插入的json数据
            index (str): 需要插入的索引
            doc_type (str, optional): 索引文档类型. Defaults to DOC_TYPE.

        Returns:
            str: 插入返回信息
        """
        info = self.es.bulk(index=index, doc_type=doc_type, body=data)

        return info

    def delete_index(self, index):
        """删除指定索引

        Args:
            index (str): 需要删除的索引

        Returns:
            str or None: 删除操作返回消息
        """
        delete_url = f'http://{self.es_host}:{self.es_port}/{index}'
        info = None
        del_info = None
        try:
            info = requests.get(self.indexes_search_url).content.decode()
        except ExternalError as e:
            lx_log.error(f'【索引删除索引查询】{e.messag}')

        if info and info.find(index) != -1:
            try:
                del_info = requests.delete(delete_url)
            except ExternalError as e:
                lx_log.error(f'【索引删除{index}】{e.messag}')

            if del_info and del_info.status_code != 200:

                return '索引删除失败'

        if info is None or del_info is None:

            return '索引删除连接es网络错误'

    def create_index(self, index, alias, mappings):
        """创建索引指定映射关系并创建别名

        Args:
            index (str): 需要创建的索引名
            alias (str): 需要创建的索引别名
            mappings (dict): 索引文档字段映射关系

        Returns:
            str: 索引创建操作返回消息
        """
        create_index_url = f'http://{self.es_host}:{self.es_port}/{index}'
        alias_data = {
            'actions': {
                'add': {
                    'index': index,
                    'alias': alias
                }
            }
        }
        index_res = None
        alias_res = None
        try:
            index_res = requests.put(create_index_url,
                                     headers=DEFAULT_HEADERS,
                                     data=json.dumps(mappings))
        except ExternalError as e:
            lx_log.error(f'【索引创建{index}】{e.messag}')

        if index_res and index_res.status_code == 200:
            try:
                alias_res = requests.put(self.alias_url,
                                         headers=DEFAULT_HEADERS,
                                         data=json.dumps(alias_data))
            except ExternalError as e:
                lx_log.error(f'【索引创建别名{index}】{e.messag}')

            if not alias_res or (alias_res and alias_res.status_code != 200):

                return '索引创建成功，别名创建失败'
        else:

            return '索引创建失败'

    def rebuild_index(self, old_index, new_index, alias, mappings):
        """重建索引并迁移旧索引数据

        Args:
            old_index (str): 旧索引索引名
            new_index (str): 新索引索引名
            alias (str): 索引别名
            mappings (dict): 索引文档字段映射关系

        Returns:
            str: 索引迁移操作返回消息
        """
        duplicate_date_url = f'http://{self.es_host}:{self.es_port}/_reindex'
        create_index_url = f'http://{self.es_host}:{self.es_port}/{new_index}'
        duplicate_date = {
            'source': {
                'index': old_index
            },
            'dest': {
                'index': new_index
            }
        }
        remove_date = {
            'actions': {
                'remove': {
                    'index': old_index,
                    'alias': alias
                }
            }
        }
        create_data = {
            'actions': {
                'add': {
                    'index': new_index,
                    'alias': alias
                }
            }
        }
        # NOTE: 先查询需删除索引和新索引是否存在
        search_res = None
        try:
            search_res = requests.get(self.indexes_search_url).content.decode()
        except ExternalError as e:
            lx_log.error(f'【索引迁移索引查询】{e.message}')

        if search_res and search_res.find(old_index) == -1:

            return '原索引不存在, 请直接创建索引'

        if search_res and search_res.find(new_index) > -1:

            return '新索引已存在, 请修改后重新操作'
        # NOTE: 创建新索引
        create_res = None
        try:
            create_res = requests.put(create_index_url,
                                      headers=DEFAULT_HEADERS,
                                      data=json.dumps(mappings))
        except ExternalError as e:
            lx_log.error(f'【索引迁移索引创建{new_index}】{e.message}')

        if not create_res or (create_res and create_res.status_code != 200):
            if create_res:
                err_msg = (json
                           .loads(create_res.content.decode())
                           .get('error')
                           .get('type'))
            else:
                err_msg = '连接网络错误'

            return f'索引迁移新索引创建失败: {err_msg}'
        # NOTE: 迁移旧索引数据至新索引
        dup_res = None
        try:
            dup_res = requests.post(duplicate_date_url,
                                    headers=DEFAULT_HEADERS,
                                    data=json.dumps(duplicate_date))
        except ExternalError as e:
            lx_log.error(f'【索引{new_index}】{e.message}')

        if not dup_res or (dup_res and dup_res.status_code != 200):
            if dup_res:
                err_msg = '数据迁移错误'
            else:
                err_msg = '连接网络错误'

            return f'索引迁移数据迁移失败: {err_msg}'
        # NOTE: 删除旧索引别名
        remove_res = None
        try:
            remove_res = requests.post(self.alias_url,
                                       headers=DEFAULT_HEADERS,
                                       data=json.dumps(remove_date))
        except ExternalError as e:
            lx_log.error(f'【索引迁移索引别名删除{new_index}】{e.message}')

        if not remove_res or (remove_res and remove_res.status_code != 200):
            if remove_res:
                err_msg = (json
                           .loads(remove_res.content.decode())
                           .get('error')
                           .get('type'))
            else:
                err_msg = '连接网络错误'

            return f'索引迁移数据迁移失败: {err_msg}'
        # NOTE: 创建新索引别名
        alias_res = None
        try:
            alias_res = requests.post(self.alias_url,
                                      headers=DEFAULT_HEADERS,
                                      data=json.dumps(create_data))
        except ExternalError as e:
            lx_log.error(f'【索引迁移索引别名创建{new_index}】{e.message}')

        if not alias_res or (alias_res and alias_res.status_code != 200):
            if alias_res:
                err_msg = (json
                           .loads(remove_res.content.decode())
                           .get('error')
                           .get('type'))
            else:
                err_msg = '连接网络错误'

            return f'索引迁移数据迁移失败: {err_msg}'

    def bulk_delete_data(self, index, doc_type, ids):
        """根据id批量删除索引数据

        Args:
            index (str): 索引名
            doc_type (str): 索引文档类型
            ids (list): 索引id列表
        """
        actions = []
        for es_id in ids:
            actions.append({
                'delete': {
                    '_index': index,
                    '_type': doc_type,
                    '_id': es_id
                }
            })
        self.es.bulk(index=index, doc_type=doc_type, body=actions)

    def get_master_node_ip(self):
        """获取主节点ip
        """
        search_url = f'http://{self.host}:{self.port}/_cat/master'
        master_node_ip = None
        try:
            res = requests.get(search_url, headers=DEFAULT_HEADERS)
            master_node_ip = res.text.split(' ')[-2]
        except (ExternalError, AttributeError, IndexError) as e:
            lx_log.error(f'【索引主节点查询】{e.message}')

        return master_node_ip


class RedisUtil:
    """连接redis相关操作
    """

    def __init__(self, config=settings.REDIS_OPTIONS, decode=True):
        """redis连接池初始化

        Args:
            config (dict, optional): 配置信息. Defaults to settings.REDIS_OPTIONS.
            decode (bool, optional): 是否对结果进行解码. Defaults to True.
        """
        self.config = config
        max_conn = self.config.get('max_connections', REDIS_MAX_CONN)
        encoding = self.config.get('encoding', REDIS_ENCODING)
        conn_params = {
            'host': self.config['HOST'],
            'port': self.config['PORT'],
            'db': self.config['DB'],
            'password': self.config['PASSWD'],
            'max_connections': max_conn
        }
        if decode is True:
            conn_params['encoding'] = encoding
            conn_params['decode_responses'] = True
        self.conn_pool = redis.ConnectionPool(**conn_params)
        self.conn_client = redis.Redis(connection_pool=self.conn_pool)
        self.mutex = threading.Lock()

    def set(self, key, value, expired_time=0):
        """redis设置字符串类型值

        Args:
            key (str): 需要设置的key
            value (optional): 需要设置的value
            expired_time (int, optional): 设置失效时间单位s. Defaults to 0.
        """
        self.conn_client.set(key, value)
        if isinstance(expired_time, int) and expired_time > 0:
            self.conn_client.expire(key, expired_time)

    def get(self, key):

        return self.conn_client.get(key)

    def delete(self, key):
        self.conn_client.delete(key)

    def rpush(self, key, value, expired_time=0):
        """执行redis列表右push操作

        Args:
            key (str): 需要push的key
            value (str): 需要push的value(数据类型是json)
            expired_time (int, optional): 设置失效时间单位s. Defaults to 0.
        """
        self.mutex.acquire()
        pipe = self.conn_client.pipeline()
        pipe.rpush(key, value)
        if isinstance(expired_time, int) and expired_time > 0:
            pipe.expire(key, expired_time)
        pipe.execute()
        self.mutex.release

    def lpush(self, key, value, expired_time=0):
        """执行redis列表左push操作

        Args:
            key (str): 需要push的key
            value (str): 需要push的value(数据类型是json)
            expired_time (int, optional): 设置失效时间单位s. Defaults to 0.
        """
        self.mutex.acquire()
        pipe = self.conn_client.pipeline()
        pipe.lpush(key, value)
        if isinstance(expired_time, int) and expired_time > 0:
            pipe.expire(key, expired_time)
        pipe.execute()
        self.mutex.release

    def rpop(self, key):

        return self.conn_client.rpop(key)

    def lpop(self, key):

        return self.conn_client.lpop(key)

    def lrange(self, key, start=0, end=-1):

        return self.conn_client.lrange(key, start, end)

    def llen(self, key):

        return self.conn_client.llen(key)

    def exists(self, key):

        return self.conn_client.exists(key)

    def public(self, channel, msg):
        """向指定通道发送消息

        Args:
            channel (str): 通道名称
            msg (str): 发送的消息
        """
        self.conn_client.publish(channel, msg)

    def subscribe(self, channel):
        """订阅指定频道的信息

        Args:
            channel (str): 通道名称
        """
        pub = self.conn_client.pubsub()
        pub.subscribe(channel)
        pub.parse_response()

        return pub
