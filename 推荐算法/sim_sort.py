"""
程序功能：
对电影相似度排序，取每部电影最接近的前一百部电影
作为最后结果，并保存进文件
"""
import pandas as pd
import numpy as np


def get_sim(filename):
    """
    对电影相似度排序，每部电影取最接近的前一百部电影
    :param filename: str, 电影之间相似度
    :return: None
    """
    sim_sort = {}  # 储存容器
    sim_data = pd.read_csv(filename)  # 读取数据
    sim_data.set_index('Unnamed: 0', inplace=True)  # 设置引索
    data_index = sim_data.index  # 获取行引索

    # 进行排序
    for data_column in sim_data.columns:
        sort_result = np.argsort(sim_data[data_column])[::-1]  # the result of sort is index of sim_data.index
        sim_sort[data_column] = [data_index[index] for index in sort_result[:100]]

    # 保存进文件
    sim_sort_df = pd.DataFrame(sim_sort)
    sim_sort_df.to_csv("sim_sort.csv")


if __name__ == '__main__':
    get_sim("movie_sim_score.csv")
