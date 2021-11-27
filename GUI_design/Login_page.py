"""
程序功能： 登录界面
"""
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QMessageBox
from tool import *


class Login_window(QMainWindow):
    def __init__(self, cur):
        super().__init__()
        self.setGeometry(100, 100, 1400, 900)  # 位置大小
        self.frame2_bar = QStatusBar()
        self.frame2_bar.setObjectName("douban")
        self.setStatusBar(self.frame2_bar)
        self.frame2_bar.showMessage("登录豆瓣")
        self.cur = cur  # 数据库游标

        # 背景颜色
        self.setStyleSheet("background-color: rgb(246, 246, 246)")

        # 登录界面图标
        set_image('image/douban.jpg', (200, 200, 400, 400), self)
        set_image('image/login_image.png', (900, 200, 400, 200), self)

        # 登录豆瓣输入框
        self.account_input = set_input_text("输入手机号码", (950, 500, 300, 40), self)

        # 密码输入框
        self.code_input = set_input_text("输入密码", (950, 550, 300, 40), self)
        self.code_input.setEchoMode(QLineEdit.Password)

        """
        设置输入栏下方按键
        """

        # 登录文字提示
        self.login = QPushButton("登录", self)
        self.login.setGeometry(950, 595, 100, 40)
        self.login.setStyleSheet("color:rgb(0, 139, 69);font-weight:bold;font-size:18px;font-family:Arial;border:none;")

        # 前往注册账号
        self.to_register = QPushButton("注册账号", self)
        self.to_register.setGeometry(1150, 595, 100, 40)
        self.to_register.setStyleSheet(
            "color:rgb(0, 139, 69);font-weight:bold;font-size:18px;font-family:Arial;border:none;")
        self.to_register.clicked.connect(self.clear)

    def judge(self, Main, main_page, main_user):
        """
        检查输入

        :param Main:
        :param main_page:
        :param main_user:
        :return:
        """
        if len(self.code_input.text()) == 0 or len(self.account_input.text()) == 0:
            QMessageBox.information(self, '提示', '请输入完全!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return  # 记得弹出弹框

        if self.account_input.text() not in self.pre_judge():
            QMessageBox.information(self, '提示', '没有该用户!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return  # 弹框
        sql = "SELECT CODE_REGISTER FROM user_data \
                WHERE PHONE = '%s' " % (self.account_input.text())
        try:
            self.cur.execute(sql)
            result = self.cur.fetchone()
        except Exception as e:
            print(e)

        if result[0] != self.code_input.text():
            QMessageBox.information(self, '提示', '密码或是账号错误!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)
            return  # 记得弹出弹框
        main_user.phone.setText('电话号码： '+self.account_input.text())
        main_page.change_status()
        Main.click_window_main()
        self.clear()

    def pre_judge(self):
        """
        返回用户清单中所有用户, 提供给judge函数
        :return:list， 用户列表
        """
        sql = "SELECT PHONE FROM user_data"
        try:
            self.cur.execute(sql)
            result = self.cur.fetchall()
        except Exception as e:
            print(e)

        all_phone = [i[0] for i in result]
        return all_phone

    def clear(self):
        # 清除输入
        self.account_input.clear()
        self.code_input.clear()


