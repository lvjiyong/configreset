# -*- coding: utf-8 -*-
import logging
import unittest

import six

from configreset import conf


class ConfTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_load_package(self):
        c = conf.load_package('etc','etc')
        print c


    def test_load(self):
        items = ['etc/setting.ini','etc/setting2.ini','etc.settings_conf']
        c = conf.load(*items)

    def test_config(self):
        conf_name = 'etc/setting.ini'
        c = conf._load_from_ini(conf_name)
        s = conf.config(c)
        self.assertEqual('127.0.0.1', s.HOST)

    def test_merge(self):
        conf_name1 = 'etc/setting.ini'
        c1 = conf._load_from_ini(conf_name1)
        self.assertEqual('80', c1.get('PORT'))
        conf_name2 = 'etc/setting2.ini'
        c2 = conf._load_from_ini(conf_name2)
        self.assertEqual('8080', c2.get('PORT'))

        c = conf.merge(c1)
        print c

    def test_merge_py(self):
        conf_name1 = 'etc.a_conf'
        c1 = conf.load_from_name(conf_name1)
        self.assertEqual('192.168.0.3', c1.get('HOST'))
        conf_name2 =  'etc.b_conf'
        c2 = conf.load_from_name(conf_name2)
        self.assertEqual('192.168.0.2', c2.get('HOST'))

    def test_load_from_name(self):
        module_name = 'etc.settings_conf'
        c = conf._load_from_module(conf._import_module(module_name))
        logging.warn(c)
        self.assertEqual('192.168.0.1', c.get('HOST'))

    def test__load_from_ini(self):
        conf_name = 'etc/setting.ini'
        c = conf._load_from_ini(conf_name)
        logging.warn(c)
        self.assertEqual('127.0.0.1', c.get('HOST'))

    def test__load_from_ini_py3(self):
        if six.PY3:
            conf_name = 'etc/setting.ini'
            c = conf._load_from_ini_py3(conf_name)
            self.assertEqual('127.0.0.1', c.get('DEFAULT').get('HOST'))

    def test__load_from_ini_py2(self):
        if six.PY2:
            conf_name = 'etc/setting.ini'
            c = conf._load_from_ini_py2(conf_name)
            self.assertEqual('127.0.0.1', c.get('HOST'))

    def test_load_from_py(self):
        module_name = 'etc.settings_conf'
        c = conf.load_from_name(module_name)
        self.assertEqual('192.168.0.1', c.get('HOST'))

    def test__import_module(self):
        module_name = 'etc.settings_conf'
        c = conf._import_module(module_name)
        self.assertEqual('192.168.0.1', c.HOST)

    def test__load_from_module(self):
        module_name = 'etc.settings_conf'
        c = conf._load_from_module(conf._import_module(module_name))
        self.assertEqual('192.168.0.1', c.get('HOST'))


if __name__ == '__main__':
    unittest.main()
