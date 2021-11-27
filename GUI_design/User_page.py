"""
程序功能： 用户界面
"""
from PyQt5.QtWidgets import QMainWindow, QMessageBox, QInputDialog
import pandas as pd
from tool import *


class User_window(QMainWindow):
    def __init__(self, cur, connect_obj):
        super().__init__()
        # 连接数据库
        self.cur = cur
        self.connect_obj = connect_obj
        self.setStyleSheet("background-color: rgb(246, 246, 246)")  # 背景颜色
        self.click_more = 0  # 点击 "更多" 按键次数
        self.movie_id = None  # 储存推荐给用户电影id，用于传给主页面

        """
        个人信息设置
        """
        # 用户照片
        set_image("image/user_normal.png", (100, 90, 250, 350), self)

        # 个人信息
        self.name = set_text("xxxxxxx", self, (450, 120, 800, 25))
        self.phone = set_text("xxxxxxx", self, (450, 200, 800, 25))
        self.mail = set_text("xxxxxxxxx", self, (450, 280, 800, 25))

        """
        设置用户喜欢的电影清单
        """
        # 设置分割线
        self.text_recommend = QLabel(self)
        self.text_recommend.setText("喜欢的电影:")
        self.text_recommend.setGeometry(20, 500, 120, 25)
        self.text_recommend.setStyleSheet("color:black;font-size:20px;font-weight:bold;font-family:Arial;border:none;")

        # 显示用户喜欢的电影图片
        self.love_image1 = set_image("image/无标题.png", (100, 540, 220, 300), self)
        self.love_image2 = set_image("image/无标题.png", (400, 540, 220, 300), self)
        self.love_image3 = set_image("image/无标题.png", (700, 540, 220, 300), self)
        self.love_image4 = set_image("image/无标题.png", (1000, 540, 220, 300), self)
        self.love_other = [self.love_image1, self.love_image2, self.love_image3, self.love_image4]

        # 用户喜欢的电影名显示
        self.love1_name = set_movie_name("xxx", self, (100, 850, 220, 20))
        self.love2_name = set_movie_name("xxx", self, (400, 850, 220, 20))
        self.love3_name = set_movie_name("xxx", self, (700, 850, 220, 20))
        self.love4_name = set_movie_name("xxx", self, (1000, 850, 220, 20))
        self.name_all = [self.love1_name, self.love2_name, self.love3_name, self.love4_name]

        """
        设置按键信号连接
        """
        # 设置"更多"按键
        self.more = QPushButton("更多", self)
        self.more.setGeometry(1250, 540, 100, 20)
        self.more.setStyleSheet("color:green;font-size:20px;font-weight:bold;font-family:Arial;border:none;")
        self.more.clicked.connect(self.change_info)

        # 设置返回键
        self.Pb_return = QPushButton("返回", self)
        self.Pb_return.setGeometry(1250, 20, 100, 40)
        self.Pb_return.clicked.connect(self.to_zero)

        # 修改密码
        self.change_code = QPushButton("修改密码", self)
        self.change_code.setGeometry(450, 360, 100, 40)
        self.change_code.clicked.connect(self.reset_code)

    def change_info(self):
        """
        修改用户界面呈现的个人信息
        :return: None
        """
        # 连接数据库，根据用户输入的手机号码搜索用户信息
        sql = "SELECT * FROM user_data \
                        WHERE PHONE = '%s' " % (self.phone.text().split("： ")[-1])
        try:
            self.cur.execute(sql)
            result = self.cur.fetchone()
        except Exception as e:
            print(e)

        # 根据搜索到的用户信息，更改用户界面呈现的信息
        self.name.setText("姓名： "+result[0])
        self.phone.setText("手机号码： "+result[1])
        self.mail.setText("邮箱： "+result[2])

        # 修改用户喜欢的电影名及其图片
        cut_result = result[-1].split()[self.click_more*4:(self.click_more + 1)*4]
        self.click_more += 1
        for index, one_id in enumerate(cut_result):
            # 连接数据库
            sql = "SELECT MOVIENAME, PICTURE FROM movie \
                          WHERE DATAID = %d " % (int(one_id))
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

        # 如果到了上限，更新为无标题图片，而且弹出弹框提示
        if len(cut_result) < 4:
            for i in range(len(cut_result), 4):
                change_picture("image/无标题/.png", self.love_other[i])
                self.name_all[i].setText("xxx")
        # 如果已经到喜欢电影列表底了，那么弹出弹框提醒
        if self.click_more*4 > len(cut_result) + 4:
            QMessageBox.information(self, '提示', '没有更多!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)

    def user_movie(self, is_not, main_movie, main_page):
        """
        接受来自电影界面的是否喜欢该电影的标志的信号，对用户喜欢电影列表进行修改
        :param is_not: int，1 代表标记为喜欢；1 代表取消喜欢
        :param main_movie: object，电影界面实例
        :param login_status: int 登录状态
        :return:None
        """
        # 如果未登录，那么弹出弹框，并结束函数
        if not main_page.login_status:
            QMessageBox.information(self, '提示', '请先登录!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return

        # 连接数据库
        sql = "SELECT MOVIE FROM user_data WHERE PHONE = '%s' " % (self.phone.text().split('： ')[1])
        try:
            self.cur.execute(sql)
            result = self.cur.fetchone()
        except Exception as e:
            print(e)

        # 判断dataID是否存在
        if main_movie.id == None:
            QMessageBox.information(self, '提示', '该电影无法标记!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return  # 弹出弹框

        # 判断点击的是哪一个标志，并作出对应行为
        if is_not:
            # 如果点击标记为喜欢，但该电影已经在用户喜欢列表中，那么提示，并终止函数
            if str(main_movie.id) in result[0].split():
                QMessageBox.information(self, '提示', '该电影已经被标记!', QMessageBox.Ok | QMessageBox.Close,
                                        QMessageBox.Close)
                return  # 弹框
            movies = result[0].split() + [str(main_movie.id)]  # 这边很奇怪没有办法直接append
        else:
            if str(main_movie.id) in result[0].split():
                movies = result[0].split()
                movies.remove(str(main_movie.id))
            else:
                # 如果点击标记为取消喜欢，但该电影并没有在用户的喜欢电影列表中，那么提示，并终止函数
                QMessageBox.information(self, '提示', '该电影不存在喜欢电影清单中!', QMessageBox.Ok | QMessageBox.Close,
                                        QMessageBox.Close)
                return  # 弹框

        # 如果前面的检测都通过了，那么修改用户的喜欢电影列表
        sql = "UPDATE user_data SET MOVIE = '%s' WHERE  PHONE = '%s'" % (" ".join(movies), self.phone.text().split('： ')[1])
        try:
            # 执行SQL语句
            self.cur.execute(sql)
            # 提交到数据库执行
            self.connect_obj.commit()
        except Exception as e:
            print(e)
            # 发生错误时回滚
            self.connect_obj.rollback()

    def get_movie_recommend(self, main_page):
        """
        接受来自主页面的推荐按键信号，提供数据给推荐系统主页
        :param main_page: object，主页面失礼了
        :return: None
        """
        # 连接数据库
        sql = "SELECT MOVIE FROM user_data \
                                WHERE PHONE = '%s' " % (self.phone.text().split("： ")[-1])
        try:
            self.cur.execute(sql)
            result = self.cur.fetchone()
        except Exception as e:
            print(e)

        # 处理推荐电影的id, 利用集合的特性去重
        set_id = set()
        result_list = result[0].split()
        recommend_id = pd.read_csv("sim_sort.csv", usecols=result_list)
        for id in result_list:
            set_id = set(recommend_id[id]) | set_id
        self.movie_id = list(set_id)

        if len(self.movie_id) == 0:
            QMessageBox.information(self, '提示', '用户无历史行为，无法做出推荐!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return
        main_page.recommend_movie(self.movie_id)

    def to_zero(self):
        """
        "更多" 按键次数清零
        :return:  None
        """
        self.click_more = 0

    def reset_code(self):
        """
        修改用户密码
        :return: None
        """
        # 弹出文本输入框
        text, ok = QInputDialog.getText(self, 'Text Input Dialog', '输入新密码：')
        if ok and text:
            # 连接数据库，修改用户密码
            sql = "UPDATE user_data SET CODE_REGISTER = '%s' WHERE  PHONE = '%s'" % (text, self.phone.text().split('： ')[1])
            try:
                # 执行SQL语句
                self.cur.execute(sql)
                # 提交到数据库执行
                self.connect_obj.commit()
            except Exception as e:
                print(e)
                # 发生错误时回滚
                self.connect_obj.rollback()
