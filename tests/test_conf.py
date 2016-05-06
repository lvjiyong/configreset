# -*- coding: utf-8 -*-
# Created by lvjiyong on 16/5/6
import unittest

from configreset import conf


class ConfTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_load_from_conf(self):
        conf_name = 'etc/setting.ini'
        c = conf._load_from_conf(conf_name)
        self.assertEqual('127.0.0.1', c.get('DEFAULT').get('host'))

    def test_load_from_conf_list(self):
        conf_name = ['etc/setting.ini', 'etc/setting2.ini']
        c = conf._load_from_conf_list(conf_name)
        self.assertEqual('8080', c.get('DEFAULT').get('port'))

    def test_load_from_name(self):
        conf_name = 'settings_conf'
        c = conf.load_from_name(conf_name)
        self.assertEqual('192.168.0.1', c.get('HOST'))


if __name__ == '__main__':
    unittest.main()