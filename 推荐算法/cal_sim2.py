"""
程序功能：
计算电影之间的相似度
"""
import pandas as pd
import numpy as np

# 电影共同出现在同一个用户的好评电影名单中的次数
movie_together_df = pd.read_csv("movie_together.csv", dtype="int32")
# 获取电影被用户评为好评的次数的数据
movie_be_clicked_df = pd.read_csv("movie_be_clicked.csv")

# 将引索设置为第一列
movie_together_df.set_index('Unnamed: 0', inplace=True)
movie_be_clicked_df.set_index('Unnamed: 0', inplace=True)

# 储存相似度容器并初始化
movie_sim_score = {}
movie_id = movie_together_df.columns
for movie_id_i in movie_id:
    movie_sim_score[movie_id_i] = {}
    for movie_id_j in movie_id:
        movie_sim_score[movie_id_i][movie_id_j] = 0.0

# 第一阶段完成
print("Fiirt event finish!")

# 计算相似度
for movie_id_i in movie_id:
    for movie_id_j in movie_id:
        if movie_be_clicked_df.loc['time'][movie_id_i] == 0 or movie_be_clicked_df.loc['time'][movie_id_j] == 0:
            movie_sim_score[movie_id_i][movie_id_j] = 0.0
            continue
        sim_socre = movie_together_df.loc[int(movie_id_j)][movie_id_i] / np.sqrt(movie_be_clicked_df.loc['time'][movie_id_i] * movie_be_clicked_df.loc['time'][movie_id_j])
        movie_sim_score[movie_id_i][movie_id_j] = sim_socre
        print(movie_id_i, movie_id_j, sim_socre)

# 第二阶段完成
print("Second event ok!")

# 储存计算结果
movie_sim_score_df = pd.DataFrame(movie_sim_score, index=movie_id, columns=movie_id, dtype="float32")
movie_sim_score_df.to_csv("movie_sim_score.csv")