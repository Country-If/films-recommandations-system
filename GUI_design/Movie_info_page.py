"""
程序功能： 电影介绍界面
"""
from PyQt5.QtWidgets import QMainWindow, QFrame
from PyQt5.QtCore import Qt
from functools import partial
import pandas as pd
from tool import *


class Movie_page(QMainWindow):
    def __init__(self, cur):
        super().__init__()
        self.setStyleSheet("background-color: rgb(246, 246, 246)")  # 背景颜色
        self.cur = cur  # 数据游标
        self.click_more = 0  # 设置“更多”选项的点击数

        # 设置页面返回键
        self.Pb_return = QPushButton("返回", self)
        self.Pb_return.setGeometry(1200, 50, 100, 40)
        self.Pb_return.clicked.connect(self.to_zero)

        """
        设置查看的电影的信息
        """

        # 电影图片
        self.image_one = set_image("image/movie_images/71.jpg", (100, 90, 250, 350), self)

        # 电影信息
        self.id = None
        self.name = set_text("xxxxxxx", self, (450, 120, 800, 25))
        self.director = set_text("xxxxxxx", self, (450, 170, 800, 25))
        self.actor = set_text("xxxxxxxxx", self, (450, 220, 800, 25))
        self.type_movie = set_text("xxxxxxx", self, (450, 270, 800, 25))
        self.score = set_text("xxxxxx", self, (450, 320, 800, 25))
        self.introduce = set_text("xxxxxxxxxx", self, (450, 370, 800, 25*2))
        self.introduce.setWordWrap(True)
        self.introduce.setAlignment(Qt.AlignTop)

        # 设置电影标记
        self.love = QPushButton("标记为喜欢", self)
        self.love.setGeometry(250, 450, 100, 30)
        self.love.setStyleSheet("color:red;font-weight:bold")
        self.not_love = QPushButton("取消标记", self)
        self.not_love.setGeometry(100, 450, 80, 30)

        """
        设置设置分割线
        """
        self.frame_tool = QFrame(self)
        self.frame_tool.setObjectName("frame_tool")
        self.frame_tool.setGeometry(0, 500, 1400, 25)
        self.frame_tool.setFrameShape(QFrame.StyledPanel)

        # 设置工具栏上的文字
        self.text_recommend = QLabel(self.frame_tool)
        self.text_recommend.setText("相关推荐")
        self.text_recommend.move(650, 0)
        self.text_recommend.resize(100, 25)
        self.text_recommend.setStyleSheet("color:red;font-size:20px;font-weight:bold;font-family:Arial;border:none;")

        """
        设置推荐电影图片以及名称
        """

        # 设置相关电影显示
        self.love1 = set_image("image/无标题.png", (100, 540, 220, 300), self)
        self.love2 = set_image("image/无标题.png", (400, 540, 220, 300), self)
        self.love3 = set_image("image/无标题.png", (700, 540, 220, 300), self)
        self.love4 = set_image("image/无标题.png", (1000, 540, 220, 300), self)
        self.love_other = [self.love1, self.love2, self.love3, self.love4]

        # 设置相关电影名显示
        self.love1_name = set_movie_name("无", self, (100, 850, 220, 20))
        self.love2_name = set_movie_name("无", self, (400, 850, 220, 20))
        self.love3_name = set_movie_name("无", self, (700, 850, 220, 20))
        self.love4_name = set_movie_name("无", self, (1000, 850, 220, 20))
        self.name_all = [self.love1_name, self.love2_name, self.love3_name, self.love4_name]
        self.names = ["" for _ in range(4)]
        for index, name in enumerate(self.name_all):
            name.clicked.connect(partial(self.to_movie_info, index, self.names))  # 连接推荐位置的电影名信号槽
            name.clicked.connect(self.to_zero)

        # 设置"更多"按键
        self.more = QPushButton("更多", self)
        self.more.setGeometry(1250, 540, 100, 20)
        self.more.setStyleSheet("color:green;font-size:20px;font-weight:bold;font-family:Arial;border:none;")
        self.more.clicked.connect(self.change_movie)

    def to_movie_info(self, index, movie_choice):
        """
        更新电影介绍界面内容
        :param index: int， movie_choice参数的引索
        :param movie_choice: list，包含电影名
        :return: None
        """
        moive_name = movie_choice[index]

        # 连接数据库
        sql = "SELECT * FROM movie \
              WHERE MOVIENAME = '%s' " % (moive_name)
        try:
            self.cur.execute(sql)
            results = self.cur.fetchone()
        except Exception as e:
            print(e)

        # 更换电影介绍界面的数据
        self.id = results[3]
        self.name.setText("电影： "+results[1])
        self.director.setText("导演： "+results[4])
        self.actor.setText("主演： "+results[5])
        self.introduce.setText("简介： "+results[13])
        self.score.setText("评分： "+str(results[11]))
        self.type_movie.setText("类型： "+"/".join(results[6:9]))
        self.introduce.setToolTip("简介： "+results[13])

        # 设置电影介绍界面的图片
        image_location = "image/movie_images/" + results[9] if results[9] != None else "image/无标题.png"
        change_picture(image_location, self.image_one)

        # 获取推荐电影的信息
        self.recommend_movie = self.recommend_info(results[3])
        self.change_movie()

    def recommend_info(self, movie_id):
        """
        根据传入的电影id，取出与其相似的电影
        :param movie_id: str，电影id
        :return: list， 推荐电影id列表
        """
        try:
            recommend_ids = pd.read_csv("sim_sort.csv", usecols=[str(movie_id)])
        except ValueError:
            return []  # 返回一个空列表，当接收到这个空列表的信号执行
        return recommend_ids[str(movie_id)].tolist()

    def change_movie(self):
        """
        更换喜欢电影信息
        :return: None
        """
        if len(self.recommend_movie) == 0:
            pass  # 执行将图片更换为无相关推荐，或者是后面有时间可以改成相同类型的电影

        ids = self.recommend_movie[self.click_more*4:(self.click_more + 1)*4]
        for index, one_id in enumerate(ids):

            # 连接数据库
            sql = "SELECT MOVIENAME, PICTURE FROM movie \
                          WHERE DATAID = %d " % (one_id)
            try:
                self.cur.execute(sql)
                results = self.cur.fetchone()
            except Exception as e:
                print(e)

            # 更换图片
            image_location = "image/movie_images/" + results[1] if results[1] != None else "image/无标题/.png"
            change_picture(image_location, self.love_other[index])

            # 更换电影名
            if len(results[0]) > 10:
                name = results[0][:10] + "..."
            else:
                name = results[0]
            self.name_all[index].setText(name)
            self.name_all[index].setToolTip(results[0])
            self.names[index] = results[0]
        self.click_more += 1

    def to_zero(self):
        # "更多"按键次数清零
        self.click_more = 0
