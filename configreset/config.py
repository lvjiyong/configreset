# -*- coding: utf-8 -*-

import logging
from importlib import import_module

import six

logger = logging.getLogger('configset')

__config = list()


def config(default_setting, project_setting):
    """
    载入项目配置，覆盖默认配置
    :param default_setting:
    :param project_setting:
    :return:
    """
    global __config

    if isinstance(default_setting, six.string_types) \
            and isinstance(project_setting, six.string_types) \
            and default_setting != project_setting:
        if project_setting not in __config:
            __config.append(project_setting)

            try:
                default_module = import_module(default_setting)
                project_module = import_module(project_setting)

                for key in dir(project_module):
                    if key.isupper():

                        value_project = value_default = None

                        if hasattr(project_module, key):
                            value_project = getattr(project_module, key)

                        if hasattr(default_module, key):
                            value_default = getattr(default_module, key)

                        if isinstance(value_project, list) and isinstance(value_default, list):

                            setattr(default_module, key, list(set(value_default).union(set(value_project))))
                        elif isinstance(value_project, dict) and isinstance(value_default, dict):

                            setattr(default_module, key, dict(value_default.items() + value_project.items()))
                        else:

                            setattr(default_module, key, value_project)

            except Exception as e:
                logger.error(e)
                pass
