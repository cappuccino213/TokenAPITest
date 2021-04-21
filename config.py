#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/4/16 9:28 
# @Author  : Zhangyp
# @File    : config.py.py
# @Software: PyCharm
# @license : Copyright(C), eWord Technology Co., Ltd.
# @Contact : yeahcheung213@163.com
import os
import configparser


class Config:
    def __init__(self, config_file='config.ini'):
        self._path = os.path.join(os.getcwd(), config_file)
        if not os.path.exists(self._path):
            raise FileNotFoundError("no such file:{}".format(config_file))
        self._config = configparser.ConfigParser(allow_no_value=True)
        self._config.read(self._path, encoding='utf-8-sig')

        # 支持插值
        self._rawConfig = configparser.RawConfigParser(allow_no_value=True)
        self._rawConfig.read(self._path, encoding='utf-8-sig')

    # raw解析
    def get_raw(self, section, name):
        return self._rawConfig.get(section, name)

    # 普通解析，返回string
    def get(self, section, name):
        return self._config.get(section, name)

    # 返回int
    def get_int(self, section, name):
        return self._config.getint(section, name)

    # 返回float
    def get_float(self, section, name):
        return self._config.getfloat(section, name)

    # 返回bool
    def get_bool(self, section, name):
        return self._config.getboolean(section, name)


cfg = Config()

if __name__ == '__main__':
    cfg = Config()
    c = cfg.get('database','ExamRequest')
    if "\n" in c:
        print("True")
        c=c.replace("\n","")
        print(c)