from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from queue import Queue
import cv2, time

Decode2Play = Queue()


class cvDecode(QThread):
    def __init__(self):
        super(cvDecode, self).__init__()
        self.threadFlag = 0  # 控制线程退出与运行
        self.video_path = ""  # 视频文件路径（后续可修改）
        self.changeFlag = 0  # 判断视频文件路径是否修改
        self.capture = 0  # 判断是否使用摄像头
        self.cap = cv2.VideoCapture()

    def run(self):
        while self.threadFlag:
            if self.changeFlag == 1 and self.video_path != "" and self.capture == 0:
                self.changeFlag = 0
                self.cap = cv2.VideoCapture(r"" + self.video_path)
            elif self.changeFlag == 1 and self.capture == 1:
                self.changeFlag = 0
                self.cap = cv2.VideoCapture(0)
            if self.video_path != "" or self.capture == 1:
                if self.cap.isOpened():
                    ret, frame = self.cap.read()
                    '''
                        对frame进行操作
                    '''
                    time.sleep(0.04)  # 控制读取录像的时间，后续可更改，但是为了防止进程混乱建议加上

                    # 控制循环播放，不需要可以删除
                    if frame is None:
                        self.cap = cv2.VideoCapture(r"" + self.video_path)

                    if ret:
                        Decode2Play.put(frame)  # 解码后的数据放入队列
                    del frame  # 释放资源
                else:
                    # 打开失败
                    if self.capture == 1:
                        self.cap = cv2.VideoCapture(0)
                    else:
                        self.cap = cv2.VideoCapture(r"" + self.video_path)
                    time.sleep(0.01)

    def load_path(self):
        self.btn_pause.setEnabled(True)

        fileName, fileType = QFileDialog.getOpenFileName(self, "选取文件", "./", "Excel Files (*.mp4);;Excel Files (*.avi)")

        self.decodework.changeFlag = 1
        self.decodework.video_path = r"" + fileName
        self.playwork.playFlag = 1

    def pause_video(self):
        if self.btn_pause.text() == "暂停":
            self.btn_pause.setText("播放")
            self.playwork.playFlag = 0
        else:
            self.btn_pause.setText("暂停")
            self.playwork.playFlag = 1


class play_Work(QThread):
    def __init__(self):
        super(play_Work, self).__init__()
        self.threadFlag = 0  # 控制线程退出
        self.playFlag = 0  # 控制播放/暂停
        self.playLabel = QLabel()  # 初始化QLabel对象

    def run(self):
        while self.threadFlag:
            if not Decode2Play.empty():
                frame = Decode2Play.get()
                if self.playFlag == 1:
                    frame = cv2.resize(frame, (760, 480), cv2.INTER_LINEAR)
                    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                    qimg = QImage(frame.data, frame.shape[1], frame.shape[0],
                                  QImage.Format_RGB888)  # 在这里可以对每帧图像进行处理，
                    self.playLabel.setPixmap(QPixmap.fromImage(qimg))  # 图像在QLabel上展示
            time.sleep(0.001)
