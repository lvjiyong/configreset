# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import logging
import sys
from collections import OrderedDict
from importlib import _resolve_name

import six

if six.PY2:
    import ConfigParser as configparser
elif six.PY3:
    import configparser

_logger = logging.getLogger('conf')

if not _logger.handlers:
    _logger = logging

_DEFAULT_SECTION = 'DEFAULT'

_CONFIG_CACHE = dict()

__all__ = ['load', 'load_setting']


def load(conf_file, default_section=_DEFAULT_SECTION):
    conf_dict = load_dict(conf_file, default_section)
    for k, v in conf_dict.items():
        pass


def load_dict(conf_file, default_section=_DEFAULT_SECTION):
    if isinstance(conf_file, list):
        return _load_from_conf_list(conf_file, default_section)
    else:
        return _load_from_conf(conf_file, default_section)


def load_from_name(module_name):
    """
    从python文件中获取配置
    :param module_name:
    :return:
    """
    settings = OrderedDict()
    if isinstance(module_name, six.string_types):
        settings = _load_from_module(_import_module(module_name))
    return settings


def _load_from_conf(conf_file, default_section=_DEFAULT_SECTION):
    global _CONFIG_CACHE
    if conf_file not in _CONFIG_CACHE:
        if six.PY3:
            _CONFIG_CACHE[conf_file] = _load_from_conf_py3(conf_file, default_section)
        else:
            _logger.error('使用PY2不支持自定义default_section')
            _CONFIG_CACHE[conf_file] = _load_from_conf_py2(conf_file)
    return _CONFIG_CACHE[conf_file]


def _load_from_conf_py2(conf_file):
    """
    从配置文件中,获取设置
    :param default_section:
    :param conf_file:
    :return:
    """
    cf = configparser.ConfigParser()
    cf.read(conf_file)
    settings = OrderedDict()
    settings['DEFAULT'] = cf.defaults()
    for section in cf.sections():
        section_dict = OrderedDict()
        for option in cf.items(section):
            section_dict[option[0]] = option[1]
        settings[section] = section_dict

    return settings


def _load_from_conf_py3(conf_file, default_section=_DEFAULT_SECTION):
    """
    从配置文件中,获取设置
    :param default_section:
    :param conf_file:
    :return:
    """

    cf = configparser.ConfigParser(default_section=default_section)
    cf.read(conf_file)
    settings = OrderedDict()
    for item in cf.items():
        settings[item[0]] = OrderedDict(item[1])
    return settings


def _load_from_conf_list(conf_list, default_section=_DEFAULT_SECTION):
    """
    从配置文件中,获取设置
    :param conf_list:
    :param default_section:
    :return:
    """
    assert isinstance(conf_list, list), 'conf_list类型必须是list'
    settings = OrderedDict()
    for conf_file in conf_list:
        single_settings = _load_from_conf(conf_file, default_section)
        for k, v in single_settings.items():
            if settings.get(k):
                settings[k].update(single_settings[k])
            else:
                settings[k] = v
    return settings


def _load_from_module(setting_module):
    """
    从python模块中获取配置
    :param setting_module:
    :return:
    """
    settings = OrderedDict()

    for key in dir(setting_module):
        if key.isupper():
            settings[key] = getattr(setting_module, key)
    return settings


def _import_module(name, package=None):
    """
    根据模块名载入模块
    :param name:
    :param package:
    :return:
    """
    if name.startswith('.'):
        if not package:
            raise TypeError("relative imports require the 'package' argument")
        level = 0
        for character in name:
            if character != '.':
                break
            level += 1

        print _resolve_name(name[level:], package, level)
        name = _resolve_name(name[level:], package, level)
    __import__(name)
    return sys.modules[name]
