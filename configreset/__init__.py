# -*- coding: utf-8 -*-
"""
载入配置文件
"""
from __future__ import unicode_literals

import json
import logging
import os
import sys
from collections import OrderedDict

import six

from .parameter import Parameter

if six.PY2:
    import ConfigParser as configparser
elif six.PY3:
    import configparser

_log_console = logging.StreamHandler(sys.stderr)
_formatter = logging.Formatter("%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s")
_log_console.setFormatter(_formatter)

logger = logging.getLogger('configreset')
logger.setLevel(logging.ERROR)
logger.addHandler(_log_console)

_DEFAULT_SECTION = 'DEFAULT'

_CONFIG_CACHE = dict()

__all__ = ['reset', 'load_package', 'logger']


def reset(target, settings):
    """
    重置设置
    :param target:
    :param settings:
    :return:
    """
    target_settings = _import_module(target)
    for k, v in settings.items():
        if hasattr(target_settings, k):
            setattr(target_settings, k, _get_value(getattr(target_settings, k), v))
        else:
            logger.debug('AttributeError {target} has no attribute {k}'.format(target=target, k=k))
    return target_settings


def load_package(package_dir, package=None, exclude=None, default_section=_DEFAULT_SECTION):
    """
    从目录中载入配置文件
    :param package_dir:
    :param package:
    :param exclude:
    :param default_section:
    :return:
    """
    init_py = '__init__.py'
    py_ext = '.py'
    files = os.listdir(package_dir)
    if init_py in files:
        files = [f for f in files if f != init_py]
        if package:
            files.insert(0, package)

    def init_package(item):
        if str(item).endswith(py_ext):
            item = item[:-3]
            if package:
                item = '{package}.{item}'.format(package=package, item=item)
        elif _is_conf(item):
            item = '{package_dir}/{item}'.format(package_dir=package_dir, item=item)
        else:
            item = package
        return str(item)

    logger.debug(files)
    files = [init_package(f) for f in files]
    if exclude:
        files = [f for f in files if f not in exclude]

    settings = load(files, default_section)
    return merge(settings)


def load(items, default_section=_DEFAULT_SECTION):
    """
    从混合类型组中读取配置
    :param default_section:
    :param items:
    :return:
    """
    settings = []

    assert isinstance(items, list), 'items必须为list'

    logger.debug(items)
    for item in items:
        if _is_conf(item):
            settings.append(load_from_ini(item, default_section))
        else:
            settings.append(load_from_name(item))
    logger.debug(settings)
    return merge(settings)



def merge(settings_list):
    """
    合并配置
    :param settings_list:
    :return:
    """
    if not isinstance(settings_list, list):
        return settings_list
    settings = OrderedDict()
    for item in settings_list:
        for k, v in item.items():
            if settings.get(k) and isinstance(v, OrderedDict):
                settings[k].update(v)
            else:
                settings[k] = v
    return settings


def config(settings):
    """
    将配置文件转为Parameter
    :param settings:
    :return:
    """
    parameter_settings = Parameter()
    for k, v in settings.items():
        if isinstance(v, OrderedDict):
            k_settings = Parameter()
            for ki, vi in v.items():
                k_settings[ki] = vi
        else:
            k_settings = v
        parameter_settings[k] = k_settings

    return parameter_settings


def load_from_name(module_name):
    """
    从python module文件中获取配置
    :param module_name:
    :return:
    """
    global _CONFIG_CACHE
    if module_name not in _CONFIG_CACHE:
        settings = OrderedDict()
        if isinstance(module_name, six.string_types):
            settings = _load_from_module(_import_module(module_name))
        _CONFIG_CACHE[module_name] = settings
    return _CONFIG_CACHE[module_name]


def load_from_ini(ini, default_section=_DEFAULT_SECTION):
    """
    从单个配置文件读取配置
    :param ini:
    :param default_section:
    :return:
    """
    global _CONFIG_CACHE
    if ini not in _CONFIG_CACHE:
        if six.PY3:
            logger.debug("PY3........")
            _CONFIG_CACHE[ini] = _load_from_ini_py3(ini, default_section)
        else:
            _CONFIG_CACHE[ini] = _load_from_ini_py2(ini)

    logger.debug(_CONFIG_CACHE[ini])
    return _CONFIG_CACHE[ini]


def _load_from_ini_py2(ini):
    """
    py2从单个配置文件中,获取设置
    :param :
    :param ini:
    :return:
    """
    logger.debug('使用PY2不支持自定义default_section，其默认值是:%s' % _DEFAULT_SECTION)
    cf = configparser.ConfigParser()
    cf.read(ini)
    settings = OrderedDict()
    for k, v in cf.defaults().items():
        settings[k.upper()] = convert_value(v)
    cf._defaults = {}
    for section in cf.sections():
        section_dict = OrderedDict()
        for option in cf.items(section):
            section_dict[option[0]] = option[1]
        settings[section] = section_dict
    return settings


def convert_value(v):
    """
    默认使用Json转化数据,凡以[或{开始的,均载入json
    :param v:
    :return:
    """
    if v and isinstance(v, six.string_types):
        v = v.strip()
        if (v.startswith('{') and v.endswith('}')) or (v.startswith('[') and v.endswith(']')):
            try:
                return json.loads(v)
            except Exception as e:
                logger.error(e)

    return v


def _load_from_ini_py3(ini, default_section=_DEFAULT_SECTION):
    """
    py3从单个配置文件中,获取设置
    :param default_section:
    :param ini:
    :return:
    """

    cf = configparser.ConfigParser(default_section=default_section)
    cf.read(ini)
    settings = OrderedDict()
    for item in cf.items():
        logger.debug(item[0])
        settings[item[0].upper()] = OrderedDict(item[1])

    logger.debug(settings)
    for k, v in cf.items(default_section):
    # for k, v in cf.items():
        logger.debug(v)
        logger.debug(settings)
        logger.debug(settings.get(k))
        settings[k.upper()] = convert_value(v)
        logger.debug(settings)
        if k.lower() in settings:
            del settings[k.lower()]

    if default_section in settings:
        del settings[default_section]

    logger.debug(settings)
    return settings


def _load_from_module(module):
    """
    从python模块中获取配置
    :param py:
    :return:
    """
    settings = OrderedDict()

    for key in dir(module):
        if key.isupper():
            settings[key] = getattr(module, key)
    return settings


def _import_module(name, package=None):
    """
    根据模块名载入模块
    :param name:
    :param package:
    :return:
    """
    if name.startswith('.'):
        name = '{package}.{module}'.format(package=package, module=str(name).strip('.'))
    __import__(name)
    return sys.modules[name]


def _is_conf(item):
    return item.endswith('.ini') or item.endswith('.conf') or item.endswith('.config')


def _get_value(first, second):
    """
    数据转化
    :param first:
    :param second:
    :return:
    >>> _get_value(1,'2')
    2
    >>> _get_value([1,2],[2,3])
    [1, 2, 3]
    """

    if isinstance(first, list) and isinstance(second, list):
        return list(set(first).union(set(second)))
    elif isinstance(first, dict) and isinstance(second, dict):
        first.update(second)
        return first
    elif first is not None and second is not None and not isinstance(first, type(second)):
        return type(first)(second)
    else:
        return second
