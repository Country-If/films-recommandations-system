"""
文件功能：放置一些各个页面之间通用的函数，方便调用
"""
from PyQt5.QtWidgets import QPushButton, QLineEdit, QLabel, QToolButton
from PyQt5.QtGui import QPixmap, QFont


def set_movie_name(text, m_f, lc_sz):
    """
    设置进入电影界面的按键，内容其实也是电影名
    :param text: 按键内容
    :param m_f: object，界面实例本身
    :param lc_sz: tuple， 位置大小
    :return: object，QPushButton实例
    """
    PB_movie_name = QPushButton(text, m_f)
    PB_movie_name.setGeometry(*lc_sz)
    PB_movie_name.setStyleSheet(
        "color:rgb(0, 139, 69);font-weight:bold;font-size:18px;font-family:Arial;border:none;")
    return PB_movie_name


def set_image(location, sz_lc, main_f):
    """
    设置图片
    :param location: str， 图片文件位置
    :param sz_lc: str， 位置大小
    :param main_f: object，界面实例本身
    :return: QLabel实例
    """
    pix1 = QPixmap(location)
    login_image1 = QLabel(main_f)
    login_image1.setGeometry(*sz_lc)
    login_image1.setPixmap(pix1)
    login_image1.setScaledContents(True)
    return login_image1


def set_input_text(text_con, sz_lc, main_f):
    """
    设置文本输入栏
    :param text_con: str，提示内容
    :param sz_lc: tuple， 位置大小
    :param main_f: object，界面实例
    :return: QLineEdit实例
    """
    account_name = QLineEdit(main_f)
    account_name.setGeometry(*sz_lc)
    account_name.setPlaceholderText(text_con)
    account_name.setFont(QFont("微软雅黑", 10))
    return account_name


def set_text(text, m_f, lc_sz):
    """
    设置文本呈现
    :param text: str, 文本内容
    :param m_f: object， 界面实例本身
    :param lc_sz: 位置大小
    :return: QLabel实例
    """
    lb = QLabel(m_f)
    lb.setGeometry(*lc_sz)
    lb.setText(text)
    lb.setStyleSheet("QLabel{color:black;font-size:20px;font-weight:bold;font-family:Arial;}")
    return lb


def change_picture(picture, movie_image):
    """
    更换电影的图片
    :param picture: str, 图片的位置（这里是相对位置）
    :param movie_image: object , 放置图片的基类 QLabel
    :return: None
    """
    movie_loc = picture
    pix241 = QPixmap(movie_loc)
    movie_image.setPixmap(pix241)


def set_btn(frame_tool, text_con, lc_sz):
    """
    设置工具栏上的按键
    :param frame_tool: object， QFrame实例
    :param text_con: 按键文本内容
    :param lc_sz: 位置
    :return: object， QToolButton实例
    """
    window_btn = QToolButton(frame_tool)
    window_btn.setCheckable(True)
    window_btn.setText(text_con)
    window_btn.setObjectName("menu_btn")
    window_btn.resize(100, 25)
    window_btn.move(*lc_sz)
    window_btn.setAutoRaise(True)
    window_btn.setStyleSheet("background-color: rgb(224, 255, 255);border:none;")
    return window_btn


def init_image_mo241(location, sz_lc, main_f):
    """
    设置八个展示电影中上半部分
    :param location: str， 图片位置
    :param sz_lc: tuple， 位置大小
    :param main_f: object，界面实例本身
    :return: object， QLabel实例
    """
    pix1 = QPixmap(location)
    login_image1 = QLabel(main_f)
    login_image1.setGeometry(sz_lc, 200, 200, 280)
    login_image1.setPixmap(pix1)
    login_image1.setScaledContents(True)
    return login_image1


def init_image_mo242(location, sz_lc, main_f):
    """
    设置八个展示电影中下半部分
    :param location: str， 图片位置
    :param sz_lc: tuple， 位置大小
    :param main_f: object，界面实例本身
    :return: object， QLabel实例
    """
    pix1 = QPixmap(location)
    login_image1 = QLabel(main_f)
    login_image1.setGeometry(sz_lc, 540, 200, 280)
    login_image1.setPixmap(pix1)
    login_image1.setScaledContents(True)
    return login_image1