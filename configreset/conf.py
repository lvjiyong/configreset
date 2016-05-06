# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from collections import OrderedDict

import six

if six.PY2:
    import ConfigParser as configparser
elif six.PY3:
    import configparser

_DEFAULT_SECTION = 'DEFAULT'

__all__ = ['load', 'load_setting']


def load_parameter(conf_file, default_section=_DEFAULT_SECTION):
    conf_dict = load_dict(conf_file, default_section)
    for k, v in conf_dict.items():
        pass


def load_dict(conf_file, default_section=_DEFAULT_SECTION):
    if isinstance(conf_file, list):
        return _load_from_conf_list(conf_file, default_section)
    else:
        return _load_from_conf(conf_file, default_section)



def _load_from_conf(conf_file, default_section=_DEFAULT_SECTION):
    if six.PY3:
        return _load_from_conf_PY3(conf_file, default_section)
    else:
        pass





def _load_from_conf_PY3(conf_file, default_section=_DEFAULT_SECTION):
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
    :param conf_file:
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


def load_setting(setting_file):
    """
    从python文件中获取配置
    :param setting_file:
    :return:
    """
