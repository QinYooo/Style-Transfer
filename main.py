import sys
import threading

from Hello import *
from PyQt5.QtWidgets import *
from Video_work import cvDecode, play_Work, socketMessage
from PyQt5.QtCore import *
from threading import Thread
import time


class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def readQss(style):
        with open(style, 'r') as f:
            return f.read()


class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)

        # # 设置窗口移动
        # self._initDrag()  # 设置鼠标跟踪判断扳机默认值
        # self.setMouseTracking(True)  # 设置widget鼠标跟踪
        # self.widget.installEventFilter(self)  # 初始化事件过滤器
        # self.widget_2.installEventFilter(self)
        # self.widget_3.installEventFilter(self)

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)  # 隐藏边框
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)  # 设置窗口背景透明
        self.render_shadow()

        # 退出按键设置
        self.close.clicked.connect(QCoreApplication.quit)
        self.hide.clicked.connect(self.showMinimized)
        # 按键事件绑定
        self.btn_input.clicked.connect(self.load_path)
        self.btn_pause.clicked.connect(self.pause_video)
        self.btn_capture.clicked.connect(self.prepare_capture)
        self.btn_style.clicked.connect(self.style)
        self.btn_pause.setEnabled(False)
        self.init_work()

    # 设置无边框和阴影效果
    def render_shadow(self):
        self.shadow = QtWidgets.QGraphicsDropShadowEffect(self)
        self.shadow.setOffset(0, 0)  # 偏移
        self.shadow.setBlurRadius(16)  # 阴影半径
        self.shadow.setColor(QtGui.QColor(128, 128, 255))  # 阴影颜色
        self.widget.setGraphicsEffect(self.shadow)  # 将设置套用到widget窗口中

    # 设置鼠标移动控制
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()

    def mouseMoveEvent(self, QMouseEvent):
        if Qt.LeftButton and self.m_flag:
            self.move(QMouseEvent.globalPos() - self.m_Position)  # 更改窗口位置
            QMouseEvent.accept()

    def mouseReleaseEvent(self, QMouseEvent):
        self.m_flag = False

    # 设置逻辑功能
    def init_work(self):
        self.decodework = cvDecode()
        self.decodework.threadFlag = 1
        self.decodework.start()

        self.playwork = play_Work()
        self.playwork.threadFlag = 1
        self.playwork.playLabel = self.label_video
        self.playwork.start()

        self.sock = socketMessage()
        self.sock.threadFlag = 1
        self.sock.start()

        self.RecvthreadFlag = 1
        self.RecvHandle()

    def style(self):
        fileName, fileType = QFileDialog.getOpenFileName(self, "选取文件", "./", "Excel Files (*.jpg);;Excel Files (*.png)")

    def prepare_capture(self):
        self.btn_pause.setEnabled(True)
        self.decodework.changeFlag = 1
        self.decodework.video_path = r""
        self.decodework.capture = 1
        self.playwork.playFlag = 1

    def load_path(self):
        self.btn_pause.setEnabled(True)

        fileName, fileType = QFileDialog.getOpenFileName(self, "选取文件", "./Flask_Http-File/save_file",
                                                         "Excel Files (*.mp4);;Excel Files (*.avi)")

        self.decodework.changeFlag = 1
        self.decodework.video_path = r"" + fileName
        self.decodework.save_name = r"" + fileName.split('/')[-1]
        self.decodework.capture = 0
        self.playwork.playFlag = 1

    def pause_video(self):
        if self.btn_pause.text() == "暂停":
            self.btn_pause.setText("播放")
            self.playwork.playFlag = 0
        else:
            self.btn_pause.setText("暂停")
            self.playwork.playFlag = 1

    def socketMaster(self):
        while self.RecvthreadFlag:
            if self.sock.Received == 1:
                time.sleep(0.4)
                fileName = "./Flask_Http-File/save_file/{}".format(self.sock.filename)
                self.decodework.changeFlag = 1
                self.decodework.video_path = r"" + fileName
                self.decodework.save_name = self.sock.name + "_{}_".format(self.sock.style) + self.sock.filename
                self.decodework.capture = 0
                self.playwork.playFlag = 1
                self.sock.Received = 0

    def closeEvent(self, event):
        print("关闭线程")
        # Qt需要先退出循环才能关闭线程
        if self.decodework.isRunning():
            self.decodework.threadFlag = 0
            self.decodework.quit()
        if self.playwork.isRunning():
            self.playwork.threadFlag = 0
            self.playwork.quit()
        if self.sock.isRunning():
            self.sock.threadFlag = 0
            self.sock.quit()
        if self.thread1.isAlive():
            self.RecvthreadFlag = 0

    def RecvHandle(self):
        self.thread1 = threading.Thread(target=MyWindow.socketMaster, args=(self,))
        self.thread1.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyWindow()
    styleFile = './style.qss'
    qssStyle = CommonHelper.readQss(styleFile)
    myWin.setStyleSheet(qssStyle)
    myWin.show()
    sys.exit(app.exec_())
