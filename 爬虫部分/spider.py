#!/usr/bin/env python
# -*- coding: UTF-8 -*-

__author__ = "Maylon"

import os
import requests
import urllib
from bs4 import BeautifulSoup
import json
import pymysql
import re

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


def parse_page(html):
    """
    解析电影界面的HTML，储存到数据库

    :param html: 电影界面的HTML
    :return: None
    """
    global image_index
    lxml_data = BeautifulSoup(html, 'lxml')
    try:
        movie_name = lxml_data.find('div', {'id': 'wrapper'}).find('div', {'id': 'content'}).find('h1').find(
            'span').text  # 电影名称
        image_url = lxml_data.find('div', {'id': 'mainpic'}).find('a', {'class': 'nbgnbg'}).find('img')['src']  # 图片url
        # 主演
        text_con = lxml_data.find('div', {'id': 'info'})
        actors_html = text_con.find('span', {'class': 'actor'}).find('span', {'class': 'attrs'}).find_all('a', {
            'rel': 'v:starring'})
        actors = [actor.text for actor in actors_html]
        actor = " ".join(actors)
        director = text_con.find('span').find('span', {'class': 'attrs'}).find('a', {'rel': 'v:directedBy'}).text  # 导演
        description = lxml_data.find('div', {'class': 'related-info'}).find('div', {'class': 'indent'}).find('span', {
            'property': 'v:summary'}).text.replace('\n', '')  # 简介
        description = re.sub(' ', '', description)
        ratingValue_str = lxml_data.find('div', {'class': "rating_self clearfix"}).find('strong',
                                                                                        {'class': 'll rating_num'}).text
        ratingValue = float(ratingValue_str)  # 评分
        picture_name = str(image_index) + ".jpg"
        if not os.path.exists("pictures"):
            os.mkdir("pictures")
        urllib.request.urlretrieve(image_url, "pictures/" + picture_name)
        image_index += 1
    except AttributeError:
        return

    # 储存进数据库
    sql = r"insert into films (movie_name, image_url, director, actor, description, ratingValue, picture)  " \
          "values ('%s', '%s', '%s', '%s', '%s', '%s', '%s');" \
          % (movie_name, image_url, director, actor, description, ratingValue, picture_name)
    try:
        cur.execute(sql)
        connect_obj.commit()
    except Exception as e:
        print(e)
        print(sql)
        connect_obj.rollback()
    print("insert movie: " + movie_name)
    # print(movie_name, image_url, director, actor, description, ratingValue)
