# -*- coding: utf-8 -*-
import logging
import unittest

import six
import configreset
from configreset import logger
logger.setLevel(logging.DEBUG)


class ConfTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_reset(self):
        c = configreset.load_package('etc', package='etc', exclude=['etc.settings_conf'])
        configreset.reset('target_conf', c)
        from . import target_conf
        self.assertEqual('127.0.0.1', target_conf.HOST)
        self.assertEqual(8080, target_conf.PORT)
        logger.debug(target_conf.MORE)

    def test_load_package_exclude(self):
        c = configreset.load_package('etc', package='etc', exclude=['etc.settings_conf'])
        self.assertEqual('8080', c.get('PORT'))
        self.assertEqual('HELLO', c.get('MORE').get('HUB'))

    def test_load_package(self):
        c = configreset.load_package('etc', 'etc', exclude=['etc'])
        self.assertEqual(8888, c.get('PORT'))
        self.assertEqual('HELLO', c.get('MORE').get('HUB'))

    def test_load(self):
        items = ['etc/setting.ini', 'etc/setting2.ini', 'etc.settings_conf']
        c = configreset.load(items)
        self.assertEqual(8888, c.get('PORT'))
        logger.debug(c)
        self.assertEqual('HELLO', c.get('MORE').get('HUB'))

    def test_config(self):
        conf_name = 'etc/setting.ini'
        c = configreset.load_from_ini(conf_name)
        s = configreset.config(c)
        self.assertEqual('127.0.0.1', s.HOST)

    def test_merge_mix(self):
        conf_name1 = 'etc.a_conf'
        c1 = configreset.load_from_name(conf_name1)
        self.assertEqual('192.168.0.3', c1.get('HOST'))
        conf_name2 = 'etc.b_conf'
        c2 = configreset.load_from_name(conf_name2)
        self.assertEqual('192.168.0.2', c2.get('HOST'))
        c = configreset.merge([c1, c2])
        logger.debug(c)

        conf_name3 = 'etc/setting.ini'
        c3 = configreset.load_from_ini(conf_name3)
        self.assertEqual('127.0.0.1', c3.get('HOST'))

        c = configreset.merge([c3, c1, c2])
        logger.debug(c)
        self.assertEqual('192.168.0.2', c.get('HOST'))

        c = configreset.merge([c1, c2, c3])
        logger.debug(c)
        self.assertEqual('127.0.0.1', c.get('HOST'))

    def test_merge(self):
        conf_name1 = 'etc/setting.ini'
        c1 = configreset.load_from_ini(conf_name1)
        self.assertEqual('80', c1.get('PORT'))
        conf_name2 = 'etc/setting2.ini'
        c2 = configreset.load_from_ini(conf_name2)
        self.assertEqual('8080', c2.get('PORT'))
        logger.debug(c2)
        c = configreset.merge([c1, c2])
        logger.debug(c)
        self.assertEqual('8080', c.get('PORT'))
        self.assertEqual('219lou', c.get('MORE').get('NAME'))
        self.assertEqual('HELLO', c.get('MORE').get('HUB'))

    def test_merge_py(self):
        conf_name1 = 'etc.a_conf'
        c1 = configreset.load_from_name(conf_name1)
        self.assertEqual('192.168.0.3', c1.get('HOST'))
        conf_name2 = 'etc.b_conf'
        c2 = configreset.load_from_name(conf_name2)
        self.assertEqual('192.168.0.2', c2.get('HOST'))
        c = configreset.merge([c1, c2])
        logger.debug(c)

    def test_load_from_name(self):
        module_name = 'etc.settings_conf'
        c = configreset._load_from_module(configreset._import_module(module_name))
        logger.debug(c)
        self.assertEqual('192.168.0.1', c.get('HOST'))

    def test__load_from_ini_py3(self):
        if six.PY3:
            conf_name = 'etc/setting.ini'
            c = configreset._load_from_ini_py3(conf_name)
            self.assertEqual('127.0.0.1', c.get('HOST'))

    def test__load_from_ini_py2(self):
        if six.PY2:
            conf_name = 'etc/setting.ini'
            c = configreset._load_from_ini_py2(conf_name)
            self.assertEqual('127.0.0.1', c.get('HOST'))

    def test_load_from_py(self):
        module_name = 'etc.settings_conf'
        c = configreset.load_from_name(module_name)
        self.assertEqual('192.168.0.1', c.get('HOST'))

    def test__import_module(self):
        module_name = 'etc.settings_conf'
        c = configreset._import_module(module_name)
        self.assertEqual('192.168.0.1', c.HOST)

    def test__load_from_module(self):
        module_name = 'etc.settings_conf'
        c = configreset._load_from_module(configreset._import_module(module_name))
        self.assertEqual('192.168.0.1', c.get('HOST'))


if __name__ == '__main__':
    unittest.main()
