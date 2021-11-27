"""
程序功能： 主要界面
"""

from PyQt5.QtWidgets import QMainWindow, QButtonGroup, QFrame, QMessageBox,\
    QStatusBar, QCompleter
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import Qt
from functools import partial
from tool import *


class window_main(QMainWindow):
    def __init__(self, cur):
        super().__init__()
        """
        主页面基本的配置
        """
        self.frame1_bar = QStatusBar()
        self.frame1_bar.setObjectName("douban")
        self.setStatusBar(self.frame1_bar)
        self.frame1_bar.showMessage("欢迎进入豆瓣")
        self.setStyleSheet("background-color: rgb(250, 253, 255)")  # 背景颜色
        self.cur = cur  # 数据库游标
        self.login_status = False  # 设置登录状态

        # 设置左上角文字
        lb = QLabel(self)
        lb.setGeometry(100, 30, 300, 100)
        lb.setText("豆 瓣 电 影")
        lb.setStyleSheet("QLabel{color:rgb(99, 184, 255);font-size:50px;font-weight:bold;font-family:Arial;}")

        """
        设置工具栏以及工具栏按键，并且连接按键的信号槽
        """

        # 工具栏
        self.frame_tool = QFrame(self)
        self.frame_tool.setObjectName("frame_tool")
        self.frame_tool.setGeometry(0, 150, 1400, 25)
        self.type_clock = [1, 0, 0, 0, 0, 0, 0]
        self.type_name = ["推荐", "剧情", "爱情", "科幻", "喜剧", "恐怖", "动作"]
        self.btn_group = QButtonGroup(self.frame_tool)

        # 工具栏选项
        window1_btn = set_btn(self.frame_tool, "推荐", (0, 0))  # "推荐"类型选项
        window2_btn = set_btn(self.frame_tool, "剧情", (120, 0))  # "剧情"类型选项
        window3_btn = set_btn(self.frame_tool, "爱情", (240, 0))  # "爱情"类型选项
        window4_btn = set_btn(self.frame_tool, "科幻", (360, 0))  # "科幻"类型选项
        window5_btn = set_btn(self.frame_tool, "喜剧", (480, 0))  # "喜剧"类型选项
        window6_btn = set_btn(self.frame_tool, "恐怖", (600, 0))  # "恐怖"类型选项
        window7_btn = set_btn(self.frame_tool, "动作", (720, 0))  # "动作"类型选项

        # 将这些选项合成一个列表, 连接信号槽并添加到工具栏
        self.window_btns = [window1_btn, window2_btn, window3_btn, window4_btn, window5_btn, window6_btn, window7_btn]
        for index, window_btn in enumerate(self.window_btns):
            window_btn.clicked.connect(partial(self.change_movie, index))
            self.btn_group.addButton(window_btn, index+1)
        self.window_btns[0].hide()  # 初始化隐藏状态

        """
        设置界面展示的电影图片和电影名
        """

        # 设置电影图片
        movie_loc = 'image/movie_images/71.jpg'  # 图片位置
        self.movie_image2414 = [init_image_mo241(movie_loc, i * 270 + 20, self) for i in range(4)]
        self.movie_image2458 = [init_image_mo242(movie_loc, i * 270 + 20, self) for i in range(4)]

        # 设置电影名称
        self.set_movie_name241 = set_movie_name("xxxxxxxxxxx", self, (20, 480, 200, 20))
        self.set_movie_name242 = set_movie_name("xxxxxxxxxxx", self, (20, 820, 200, 20))
        self.set_movie_name243 = set_movie_name("xxxxxxxxxxx", self, (290, 480, 200, 20))
        self.set_movie_name244 = set_movie_name("xxxxxxxxxxx", self, (290, 820, 200, 20))
        self.set_movie_name245 = set_movie_name("xxxxxxxxxxx", self, (560, 480, 200, 20))
        self.set_movie_name246 = set_movie_name("xxxxxxxxxxx", self, (560, 820, 200, 20))
        self.set_movie_name247 = set_movie_name("xxxxxxxxxxx", self, (830, 480, 200, 20))
        self.set_movie_name248 = set_movie_name("xxxxxxxxxxx", self, (830, 820, 200, 20))

        # 将这些按键组成一个列表
        self.set_movie_name = [self.set_movie_name241, self.set_movie_name243, self.set_movie_name245,
                               self.set_movie_name247, self.set_movie_name242, self.set_movie_name244,
                               self.set_movie_name246, self.set_movie_name248]

        # 初始化主页面的电影图片和名称
        self.movie_choice = [" " for _ in range(8)]  # 储存显示的八个电影名，方便查找
        self.change_movie(1)

        """
        设置搜索输入栏，搜索按键，以及登录、注册 按键
        """

        # 设置文本输入栏——搜索电影
        self.movie_input = QLineEdit(self)
        self.movie_input.setGeometry(400, 65, 300, 30)
        self.movie_input.setPlaceholderText("搜索电影")
        self.init_search(self.get_all_name())  # 设置模糊搜索

        # 设置搜索图标
        self.pb_search = QPushButton(self)
        self.pb_search.setGeometry(700, 65, 30, 30)
        self.pb_search.setIcon(QIcon("image/search.png"))

        # 设置登录、注册
        self.pb_login, self.pb_register = QPushButton("登录", self), QPushButton("注册", self)
        self.pb_login.setGeometry(1200, 65, 40, 30)
        self.pb_register.setGeometry(1250, 65, 40, 30)

    def init_search(self, all_names):
        """
        设置模糊搜索模式
        :param all_names: list，包含数据库中所有电影名，由get_all_name函数获取
        :return: None
        """
        self.completer = QCompleter(all_names)  # 增加自动补全
        self.completer.setFilterMode(Qt.MatchContains)  # 设置匹配模式
        self.completer.setCompletionMode(QCompleter.PopupCompletion)  # 设置补全模式
        self.movie_input.setCompleter(self.completer)  # 给文本输入框设置补全器

    def get_all_name(self):
        """
        获取数据库中所有的电影名，提供给模糊搜索
        :return: list， 储存电影名
        """
        # 连接数据库获取数据
        sql = "SELECT MOVIENAME FROM movie"
        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
        except Exception as e:
            print(e)

        # 获取所有电影名称，并处理好格式
        movie_names = [i[0] for i in results]

        return movie_names

    def change_movie(self, type):
        """
        用来修改除了 "推荐" 选项外，其他类型电影的信息更新
        :param type: int，输入按键的引索，例如点击 "剧情" 则输入 "1"
        :return: None
        """
        # 判断点击的是哪一个类型, 如果是'推荐'，那么取消
        if self.type_clock[type] == 0:
            self.type_clock = [0 for _ in range(7)]
            self.type_clock[type] += 1
        if type == 0:
            return

        # 连接数据库获取数据
        sql = "SELECT MOVIENAME, PICTURE FROM movie \
              WHERE TYPE1 = '%s' or TYPE2 = '%s' or TYPE3 = '%s' " % \
              (self.type_name[type], self.type_name[type], self.type_name[type])
        try:
            self.cur.execute(sql)
            results = self.cur.fetchall()
            lc_name = results[self.type_clock[type]*8:(self.type_clock[type] + 1)*8]
        except Exception as e:
            print(e)
        self.type_clock[type] += 1  # 该类型访问次数加一

        # 修改电影图片,名称
        movie_image24 = self.movie_image2414 + self.movie_image2458
        for index, (movie_image, lc_image, movie_name) in enumerate(zip(movie_image24, list(lc_name), self.set_movie_name)):
            image_location = "image/movie_images/" + lc_image[1] if lc_image[1] != None else "image/无标题.png"
            change_picture(image_location, movie_image)
            if len(lc_image[0]) > 10:
                name = lc_image[0][:10] + "..."
            else:
                name = lc_image[0]
            movie_name.setText(name)
            movie_name.setToolTip(lc_image[0])
            self.movie_choice[index] = lc_image[0]

    def recommend_movie(self, movie_ids):
        """
        点击 "推荐" 按键时，更新主页面的电影信息
        :param movie_ids: 推荐的电影的dataID
        :return: None
        """
        # 连接数据库获取推荐电影数据
        results = []
        for id in movie_ids[self.type_clock[0]*8:(self.type_clock[0] + 1)*8]:
            sql = "SELECT MOVIENAME, PICTURE FROM movie \
                                  WHERE DATAID = %s " % \
                  (int(id))
            try:
                self.cur.execute(sql)
                results.append(self.cur.fetchone())
            except Exception as e:
                print(e)
        self.type_clock[0] += 1  # 点击次数加一

        # 修改电影图片,名称
        movie_image24 = self.movie_image2414 + self.movie_image2458
        for index, (movie_image, lc_image, movie_name) in enumerate(
                zip(movie_image24, results, self.set_movie_name)):
            image_location = "image/movie_images/" + lc_image[1] if lc_image[1] != None else "image/无标题/.png"
            change_picture(image_location, movie_image)
            if len(lc_image[0]) > 10:
                name = lc_image[0][:10] + "..."
            else:
                name = lc_image[0]
            movie_name.setText(name)
            movie_name.setToolTip(lc_image[0])
            self.movie_choice[index] = lc_image[0]

    def to_movie_info(self, main_movie, Main):
        """
        接受来自电影搜索输入栏的信号，判断是否符合条件，如果符合则进入电影介绍界面
        :param main_movie: object， 电影界面实例
        :param Main: object， 载体界面实例
        :return:None
        """
        if self.movie_input.text() in self.get_all_name():
            main_movie.to_movie_info(0, [self.movie_input.text()])
            Main.click_window_movie()
            self.clear()
        else:
            QMessageBox.information(self, '提示', '没有这一部电影!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)

    def change_status(self):
        """
        接受登录界面信号，改变主页面登录状态
        :return: None
        """
        self.login_status = True
        self.pb_login.setText("主页")
        self.pb_register.setText("退出")
        self.window_btns[0].show()

    def to_login_user(self, Main, main_user):
        """
        在未登录状态下，左上角靠左边的按键显示为 “登录”
        在登录状态下，该按键显示为 “主页”

        函数功能：接受该按键的信号，判断并进入对应界面
        :param Main: object，载体页面实例
        :param main_user: object， 用户界面实例
        :return:None
        """
        if self.login_status:
            main_user.change_info()
            Main.click_window_user()
            self.clear()
        else:
            Main.click_window_login()

    def to_register_quit(self, Main):
        """
        在未登录状态下，左上角靠右边的按键显示为 “注册”
        在登录状态下，该按键显示为 “退出”

        函数功能：接受该按键的信号，判断并进入对应界面
        :param Main: object， 载体界面实例
        :return: None
        """
        if self.login_status:
            self.login_status = False
            self.pb_login.setText("登录")
            self.pb_register.setText("注册")
            self.window_btns[0].hide()
        else:
            Main.click_window_register()

    def clear(self):
        self.movie_input.clear()
