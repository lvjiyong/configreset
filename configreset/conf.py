# -*- coding: utf-8 -*-
"""
载入配置文件
"""
from __future__ import unicode_literals

import logging
import os
import sys
from collections import OrderedDict

import six

from configreset.parameter import Parameter

if six.PY2:
    import ConfigParser as configparser
elif six.PY3:
    import configparser

_logger = logging.getLogger('configreset')

if not _logger.handlers:
    _logger = logging

_DEFAULT_SECTION = 'DEFAULT'

_CONFIG_CACHE = dict()

__all__ = ['load', 'load_setting']


def load_package(package_dir, package=None, exclude=None):
    init_py = '__init__.py'
    py_ext = '.py'
    files = os.listdir(package_dir)

    if exclude:
        files = [f for f in files if f not in exclude]

    if init_py in files:
        files = [f for f in files if f != init_py]
        if package:
            files.insert(0,package)

    def init_package(item):
        if str(item).endswith(py_ext):
            item = item.strip('.py')
            if package:
                item = '{package}.{item}'.format(package=package, item=item)
        return str(item)

    files = [init_package(f) for f in files]
    return merge(load(*files))


def load(items, default_section=_DEFAULT_SECTION):
    """
    从混合类型组中读取配置
    :param items:
    :return:
    """
    settings = []
    for item in items:
        print item
        if item.startswith('ini:') or item.endswith('.ini') or item.endswith('.conf') or item.endswith('.config'):
            settings.append(load_from_ini(item.strip('ini:')))
        else:
            settings.append(load_from_name(item))
        print settings
    print settings
    return merge(settings)


def merge(*settings_list):
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
            if settings.get(k):
                settings[k].update(item[k])
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


def load_from_ini(ini, default_section=_DEFAULT_SECTION):
    """
    从单个或多个配置文件读取配置
    :param ini: string单个，list多个
    :param default_section:
    :return:
    """
    if isinstance(ini, list):
        setttings_list = []
        for item in ini:
            setttings_list.append(_load_from_ini(ini, default_section))
            return merge(item, default_section)
    else:
        return _load_from_ini(ini, default_section)


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


def _load_from_ini(ini, default_section=_DEFAULT_SECTION):
    """
    从单个配置文件读取配置
    :param ini:
    :param default_section:
    :return:
    """
    global _CONFIG_CACHE
    if ini not in _CONFIG_CACHE:
        if six.PY3:
            _CONFIG_CACHE[ini] = _load_from_ini_py3(ini, default_section)
        else:
            _CONFIG_CACHE[ini] = _load_from_ini_py2(ini)
    return _CONFIG_CACHE[ini]


def _load_from_ini_py2(ini):
    """
    py2从单个配置文件中,获取设置
    :param :
    :param ini:
    :return:
    """
    _logger.debug('使用PY2不支持自定义default_section')
    default_section = 'DEFAULT'
    cf = configparser.ConfigParser()
    cf.read(ini)
    logging.warn(cf.items('M'))


    settings = OrderedDict()
    for k, v in cf.defaults().items():
        settings[k.upper()] = v

    logging.warn(settings)

    print cf.items('M')
    for section in cf.sections():
        logging.warn(section)
        section_dict = OrderedDict()

        for option in cf.options(section):
            logging.warn(option)
            section_dict[option[0].upper()] = option[1]
        settings[section] = section_dict
    if default_section in settings:
        del settings[default_section]
    return settings


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
        settings[item[0].upper()] = OrderedDict(item[1])

    for k, v in cf.get(default_section).items():
        settings[k.upper()] = v
    if default_section in settings:
        del settings[default_section]
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
