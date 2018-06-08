# -*- coding: utf-8 -*-
import urllib.request
import os
from time import *
from urllib import parse
from selenium import webdriver
import logging


def save_pictures(path, url_list, opener):
    """
    保存图片到本地指定文件夹
    :param path: 保存图片的文件夹，由mkdir_for_girl返回
    :param url_list: 待保存图片的url列表
    :param opener: urllib传递的输入句柄
    :return: none
    """
    for (index, url) in enumerate(url_list):
        words = url.split("/")
        pic_name = words[len(words)-1].replace("_master1200", "")
        file_name = os.path.join(path, pic_name)
        # 如果存在该图片则不保存
        if os.path.exists(file_name):
            continue
        req = urllib.request.Request(url)
        try:
            data = opener.open(req, timeout=30).read()
            f = open(file_name, 'wb')
            f.write(data)
            f.close()
        except Exception as e:
            logging.warning("异常：" + str(e))


# ------------定义3个函数，用来创建每个girl的目录、保存图片、写入文本描述及对话----------------
def mkdir_for_girl(f_path):
    """
    创建以标题命令的目录
    :param f_path: 文件根路径
    :return: 返回创建的目录路径
    """
    if not os.path.exists(f_path):
        os.mkdir(f_path)
    return f_path


def get_url(driver, word):
    url = "http://image.baidu.com/search/index?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&word=" \
          + parse.quote(word)
    driver.get(url)
    sleep(1)
    urls = []
    try:
        imgele = driver.find_element_by_class_name("imgpage")
        imgs = imgele.find_elements_by_class_name("imgitem")
        for img in imgs:
            url = img.get_attribute("data-objurl")
            urls.append(url)
    except Exception as e:
        print("无法搜索"+word)
    return urls


def start():
    base_file = "e:/pic/"
    browser = webdriver.Chrome("d:/chromedriver.exe")
    file = open("./name.txt", encoding="utf-8")
    line = file.readline().replace("\n", "")
    opener = urllib.request.build_opener()
    while line is not '':
        urls = get_url(browser, line)
        save_pictures(mkdir_for_girl(base_file+line), urls, opener)
        line = file.readline().replace("\n", "")
    file.close()


start()
