"""
程序功能： 注册界面
"""
from PyQt5.QtWidgets import QMainWindow, QStatusBar, QMessageBox
from tool import *


class register_page(QMainWindow):
    def __init__(self, connect_obj, cur):
        super().__init__()
        # 数据库连接和游标
        self.connect_obj = connect_obj
        self.cur = cur

        self.frame3_bar = QStatusBar()
        self.frame3_bar.setObjectName("douban")
        self.setStatusBar(self.frame3_bar)
        self.frame3_bar.showMessage("注册豆瓣账号")

        # 背景颜色
        self.setStyleSheet("background-color: rgb(246, 246, 246)")

        # 设置注册界面的图片
        set_image('image/douban.jpg', (200, 200, 400, 400), self)
        set_image('image/login_image.png', (900, 100, 400, 200), self)

        """
        设置注册信息输入栏
        """

        self.account_name = set_input_text("输入账号", (950, 400, 300, 40), self)  # 账号名称
        self.phone = set_input_text("输入手机号码", (950, 450, 300, 40), self)  # 手机号
        self.mail = set_input_text("输入邮箱", (950, 500, 300, 40), self)  # 邮箱
        self.code_register = set_input_text("输入密码", (950, 550, 300, 40), self)  # 设置密码
        self.code_real = set_input_text("再次输入密码", (950, 600, 300, 40), self)  # 确认密码
        self.code_real.setEchoMode(QLineEdit.Password)
        self.code_register.setEchoMode(QLineEdit.Password)
        self.infos = [self.account_name, self.phone, self.mail, self.code_register, self.code_real]  # 对输入内容进行判别

        """
        设置输入栏下方按键
        """

        # “注册”按键
        self.Pb_register = QPushButton("注册", self)
        self.Pb_register.setGeometry(950, 650, 100, 40)
        self.Pb_register.setStyleSheet("color:rgb(0, 139, 69);font-weight:bold;font-size:18px;font-family:Arial;border:none;")

        # 已有账号前往登录
        self.to_login = QPushButton("已有账号前往登录", self)
        self.to_login.setGeometry(1050, 650, 200, 40)
        self.to_login.setStyleSheet("color:rgb(0, 139, 69);font-weight:bold;font-size:18px;font-family:Arial;border:none;")
        self.to_login.clicked.connect(self.clear)

    def judge(self, Main):
        """
        简单的信息核实
        :param Main:
        :return:
        """
        # 检测是否有全部填写
        input_context = [info.text() for info in self.infos]
        if not all(input_context):
            QMessageBox.information(self, '提示', '请输入完全!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)

        if self.code_register.text() != self.code_real.text():
            QMessageBox.information(self, '提示', '前后两次密码输入不一致!', QMessageBox.Ok | QMessageBox.Close,
                                    QMessageBox.Close)

        if self.code_register.text() == self.code_real.text() and all(input_context):
            # 如果通过检测那么就执行将数据保存的函数
            self.save_data()
            Main.click_window_login()
            self.clear()

    def save_data(self):
        """
        将注册信息保存到数据库中
        :return: None
        """
        sql = "\
            INSERT INTO user_data(account_name, phone, mail, code_register, movie) \
            VALUES('%s', '%s', '%s', '%s', '%s')" % (self.account_name.text(), self.phone.text(), self.mail.text(), self.code_register.text(), "")

        try:
            self.cur.execute(sql)
            self.connect_obj.commit()
        except Exception as e:
            print(e)
            self.connect_obj.rollback()

    def clear(self):
        # 清除输入
        for info in self.infos:
            info.clear()