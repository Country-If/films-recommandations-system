"""
文件功能：提供一个QWidget类作为载体加载其他页面
"""

from sshtunnel import SSHTunnelForwarder
from PyQt5.QtWidgets import QApplication, QFrame, QStackedLayout, QWidget
from PyQt5.QtGui import QIcon
from functools import partial
import pymysql
from Main_page import window_main
from Movie_info_page import Movie_page
from User_page import User_window
from Login_page import Login_window
from Register import register_page
import sys


class Main(QWidget):
    def __init__(self):
        super().__init__()
        self.__setup_ui__()

    def __setup_ui__(self):
        """
        载体界面
        :return: None
        """

        """
        载体界面的简单配置
        """
        self.setGeometry(0, 0, 1400, 900)  # 位置大小
        self.setWindowTitle("模拟豆瓣")  # 应用名称
        self.setWindowIcon(QIcon("image/douban.jpg"))  # 设置图标

        # 工作区域
        self.main_frame = QFrame(self)
        self.main_frame.setGeometry(0, 0, self.width(), self.height())

        # 创建堆叠布局
        self.stacked_layout = QStackedLayout(self.main_frame)

        # 通过SSH连接云服务器
        server = SSHTunnelForwarder(
            ssh_address_or_host=('120.79.14.209', 22),  # 云服务器地址IP和端口port
            ssh_username='mysql_db',  # 云服务器登录账号
            ssh_password='mysql_db',  # 云服务器登录密码
            remote_bind_address=('localhost', 3306)  # 数据库服务地址ip,一般为localhost和端口port，一般为3306
        )
        # 云服务器开启
        server.start()
        # 云服务器上mysql数据库连接
        self.connect_obj = pymysql.connect(host='127.0.0.1',  # 此处必须是是127.0.0.1
                                           port=server.local_bind_port,
                                           user='software_engineer',  # mysql的登录账号
                                           password='mysql_db',  # mysql的登录密码
                                           db='films_system_db',  # mysql中要访问的数据库
                                           charset='utf8')  # 表的字符集

        # 与本地数据库建立连接
        # self.connect_obj = pymysql.connect(host='localhost', user='root', password='root', database='films_system_db',
        #                               port=3306)
        self.cur = self.connect_obj.cursor()  # 获取游标

        """
        加载各个界面
        """
        self.main_page = window_main(self.cur)  # 主页面
        self.main_login = Login_window(self.cur)  # 登录页面
        self.main_register = register_page(self.connect_obj, self.cur)  # 注册账号界面
        self.main_movie = Movie_page(self.cur)  # 电影界面
        self.main_user = User_window(self.cur, self.connect_obj)  # 个人界面

        # 把五个界面实例加入到堆叠布局中
        self.stacked_layout.addWidget(self.main_page)
        self.stacked_layout.addWidget(self.main_login)
        self.stacked_layout.addWidget(self.main_register)
        self.stacked_layout.addWidget(self.main_movie)
        self.stacked_layout.addWidget(self.main_user)

        """
        主页面信号槽连接
        """
        # 连接电影名信号槽，响应进入电影介绍界面
        for index, movie_name_Pb in enumerate(self.main_page.set_movie_name):
            movie_name_Pb.clicked.connect(partial(self.main_movie.to_movie_info, index, self.main_page.movie_choice))
            movie_name_Pb.clicked.connect(self.click_window_movie)
            movie_name_Pb.clicked.connect(self.main_page.clear)

        # 连接搜索的信号槽，响应进入电影介绍界面
        self.main_page.movie_input.returnPressed.connect(
            partial(self.main_page.to_movie_info, self.main_movie, self))
        self.main_page.pb_search.clicked.connect(partial(self.main_page.to_movie_info, self.main_movie, self))

        # 连接登录和注册按键信号槽
        self.main_page.pb_register.clicked.connect(partial(self.main_page.to_register_quit, self))
        self.main_page.pb_login.clicked.connect(partial(self.main_page.to_login_user, self, self.main_user))

        # 连接推荐位置的按键信号槽
        self.main_page.window_btns[0].clicked.connect(partial(self.main_user.get_movie_recommend, self.main_page))

        """
        登录界面信号槽连接
        """
        # 连接输入密码回车信号槽
        self.main_login.code_input.returnPressed.connect(
            partial(self.main_login.judge, self, self.main_page, self.main_user))

        # 连接“前往注册界面”信号槽
        self.main_login.to_register.clicked.connect(self.click_window_register)
        self.main_login.login.clicked.connect(partial(self.main_login.judge, self, self.main_page, self.main_user))

        """
        注册界面信号槽连接
        """
        # 连接"注册" "前往登录界面" 信号槽
        self.main_register.to_login.clicked.connect(self.click_window_login)
        self.main_register.Pb_register.clicked.connect(partial(self.main_register.judge, self))

        """
        个人界面信号槽连接
        """
        # 连接返回键信号槽
        self.main_user.Pb_return.clicked.connect(self.click_window_main)

        """
        电影界面信号槽连接
        """
        # 连接返回键信号槽
        self.main_movie.Pb_return.clicked.connect(self.click_window_main)

        # 设置电源界面标志喜欢或者不喜欢的标记的信号槽的连接
        self.main_movie.love.clicked.connect(partial(self.main_user.user_movie, 1, self.main_movie, self.main_page))
        self.main_movie.not_love.clicked.connect(partial(self.main_user.user_movie, 0, self.main_movie, self.main_page))

    """
    五个子函数，分别对应进入五个界面
    """

    def click_window_main(self):
        """
        进入主界面
        :return: None
        """
        self.stacked_layout.setCurrentIndex(0)
        self.main_page.frame1_bar.showMessage("欢迎进入豆瓣")

    def click_window_login(self):
        """
        进入登录界面
        :return: None
        """
        self.stacked_layout.setCurrentIndex(1)
        self.main_login.frame2_bar.showMessage("登录豆瓣")

    def click_window_register(self):
        """
        进入注册界面
        :return: None
        """
        self.stacked_layout.setCurrentIndex(2)
        self.main_register.frame3_bar.showMessage("注册豆瓣账号")

    def click_window_movie(self):
        """
        进入电影介绍界面
        :return: None
        """
        self.stacked_layout.setCurrentIndex(3)

    def click_window_user(self):
        """
        进入用户界面
        :return: None
        """
        self.stacked_layout.setCurrentIndex(4)


if __name__ == "__main__":
    app = QApplication(sys.argv)  # 创建图形用户对象
    window = Main()  # 载体实例
    window.show()
    sys.exit(app.exec_())  # 接受返回状态码，结束进程
