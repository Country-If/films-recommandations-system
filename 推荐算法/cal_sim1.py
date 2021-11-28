"""
程序功能：
计算每一个电影被用户评为好评的次数，以及不同电影共同出现在同一个用户的喜欢电影di数据次数
相似度计算前期铺垫
"""
import pandas as pd
import numpy as np
import threading
import pymysql


def get_id():
    """
    获取电影的ID
    :return: list, 元素为电影ID的列表
    """
    # 与数据库建立连接
    connect_obj = pymysql.connect(host='localhost', user='root', password='1231', database='check_qg_data', port=3306)
    cur = connect_obj.cursor()  # 获取游标

    sql = "SELECT DATAID FROM MOVIE_QG"
    try:
        cur.execute(sql)  # 执行SQL语句
        results = cur.fetchall()  # 获取所有记录列表
        data_id = []
        for data in results:
            if data[0] == None:  # 如果是缺失值就舍弃
                continue
            data_id.append(data[0])

    except Exception as e:
        print(e)
        print("Error: unable to fetch data")

    connect_obj.close()  # 关闭数据库连接
    return data_id


def select(user_love, user_click, index_num_l, index_num_r):
    """
    线程的目标函数，获取指定范围内用户喜欢的电影的id
    :param user_love: DataFrame，经过筛选后的ratings.csv数据集
    :param user_click: dict, 储存用户喜欢的电影id
    :param index_num_l: int, 范围左边界
    :param index_num_r: int, 范围右边界
    :return: None
    """
    for user_id in range(index_num_l, index_num_r):
        love_movie_id = user_love[user_love['userId'] == user_id+1]['movieId']  # 获取每一个用户喜欢的电影
        user_click[user_id+1] = love_movie_id.tolist()  # 每个用户添加其比较喜欢的电影


def get_click(file_name):
    """
    获取所有用户喜欢的电影的id
    :param file_name: str, MovieLens数据集中的ratings.csv数据
    :return: {
                user_click: dict, 储存所有用户喜欢电影的id
                movie_id: list, 加载的有交集部分的电影id
            }
    """
    # 加载电影Id
    movie_id = get_id()

    # 对MovieLens数据集中的ratings.csv数据进行处理
    user_data = pd.read_csv(file_name, dtype="float32")
    user_love = user_data[user_data["rating"] >= 3.5]  # 评分低于3.5分的忽略,不认为用户喜欢这部电影
    user_love = user_love[user_love["movieId"].isin(movie_id)]  # 选择属于交集部分的数据
    max_user_id = np.max(user_love['userId'])  # 获得用户的数量

    # 启动多线程，获取所有用户喜欢的电影id
    user_click = {}
    threads = []
    time = 8  # 设置线程数量
    index_num = int(max_user_id/time)  # 获取每一段范围内的用户数量，注意最后一段需要额外处理
    for i in range(time-1):
        t = threading.Thread(target=select, args=(user_love, user_click, index_num*i, index_num*(i+1)))
        threads.append(t)
        t.start()
    t = threading.Thread(target=select, args=(user_love, user_click, index_num*(time-1), int(max_user_id)))
    threads.append(t)
    t.start()

    # 等所有线程走完再进行下一步
    for t in threads:
        t.join()

    print("数据加载完毕")
    # 以字典格式返回用户喜爱电影Id
    return user_click, movie_id


def cal_similarity(user_click, movie_id):
    """
    计算每一个电影被用户评为好评的次数，以及不同电影共同出现在同一个用户的喜欢电影di数据次数
    :param user_click: dict, 每一个用户喜欢的电影id
    :param movie_id: list, 有交集部分的电影id
    :return:{
                movie_be_clicked: dict, 储存一个电影被用户评为好评的次数
                movie_together: dict, 储存不同电影共同出现在同一个用户的喜欢电影di数据次数
            }
    """
    # 设置储存容器，并初始化
    movie_be_clicked = {}  # 存储每一个电影被用户评为好评的次数
    movie_together = {}  # 储存电影共同出现在同一个用户的好评电影名单中的次数
    for movie_id_i in movie_id:
        movie_be_clicked[movie_id_i] = 0
        movie_together[movie_id_i] = {}
        for movie_id_j in movie_id:
            movie_together[movie_id_i][movie_id_j] = 0

    # 开始计算
    for movie_id_list in user_click.values():  # 获取每一个用户的喜欢电影id列表
        # 计算每一个电影被用户评为好评的次数
        for movie_index_i in range(len(movie_id_list)):
            movie_id_i = movie_id_list[movie_index_i]
            movie_be_clicked[movie_id_i] += 1  # 电影被评过好评次数加一

            # 计算电影共同出现在同一个用户的好评电影名单中的次数
            for movie_index_j in range(movie_index_i+1, len(movie_id_list)):
                movie_id_j = movie_id_list[movie_index_j]
                movie_together[movie_id_i][movie_id_j] += 1
                movie_together[movie_id_j][movie_id_i] += 1

    print("相似度第一步计算完毕")
    return movie_together, movie_be_clicked


if __name__ == '__main__':
    file_n = "ratings.csv"
    user_c, movie_id = get_click(file_n)
    movie_together, movie_be_clicked = cal_similarity(user_c, movie_id)

    # 存进文件
    movie_be_clicked_df = pd.DataFrame(movie_be_clicked, index=['time'], dtype="int32")
    movie_be_clicked_df.to_csv("movie_be_clicked.csv")
    movie_together_df = pd.DataFrame(movie_together, dtype="int16")
    movie_together_df.to_csv("movie_together.csv")
