#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import requests
import json
import pymysql


Headers = {
    'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                  "(KHTML, like Gecko) Chrome/80.0.3987.131 Safari/537.36"
}
# 与数据库建立连接
connect_obj = pymysql.connect(host='localhost', user='root', password='root', database='films_system_db', port=3306)
cur = connect_obj.cursor()  # 获取游标
image_index = 0


def get_html(url, headers):
    """
    解析每一页XHR，获取进入电影介绍界面的url，获取HTML存到列表中

    :param url:XHR文件URL
    :param headers:请求头
    :return:每页加载的二十部电影主页的HTML代码
    """
    # 发送请求
    resp = requests.get(url, headers=headers)
    # 转化为字典形式
    resp_dict = json.loads(resp.text)
    # 获取各个电影信息组成的列表，列表中每一个电影的信息是一个字典
    info_list = resp_dict['subjects']
    # 获取各个电影主页面的url
    url_list = [info['url'] for info in info_list]

    htmls = []
    for u in url_list:
        resp_u = requests.get(u, headers=headers)
        htmls.append(resp_u.text)
    return htmls

