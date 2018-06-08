# -*- coding: utf-8 -*-
import urllib.request
import os
from time import *
from urllib import parse
from selenium import webdriver
import logging


# ------------定义3个函数，用来创建每个girl的目录、写入文本描述及对话----------------
def mkdir_for_girl(f_path):
    """
    创建以标题命令的目录
    :param f_path: 文件根路径
    :return: 返回创建的目录路径
    """
    if not os.path.exists(f_path):
        os.mkdir(f_path)
    return f_path

for i in range(1, 10):
    print(i)
