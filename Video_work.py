from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from queue import Queue
import cv2
import time
import json
from socket import *
import os

HOST = "127.0.0.1"
PORT = 8888
BUFIZ = 1024
ADDR = (HOST, PORT)

# socket element
ifReceived = 0

Decode2Play = Queue()


class cvDecode(QThread):
    def __init__(self):
        super(cvDecode, self).__init__()
        self.threadFlag = 0  # 控制线程退出与运行
        self.video_path = ""  # 视频文件路径（后续可修改）
        self.changeFlag = 0  # 判断视频文件路径是否修改
        self.capture = 0  # 判断是否使用摄像头
        self.cap = cv2.VideoCapture()
        self.path = os.getcwd() + '/Flask_Http-File/translate_file'
        self.fourcc = cv2.VideoWriter_fourcc('M', 'P', '4', 'V')
        self.fps = 30
        self.width = 0
        self.height = 0
        self.save_name = ""

    def run(self):
        while self.threadFlag:
            if self.changeFlag == 1 and self.video_path != "" and self.capture == 0:
                self.changeFlag = 0
                self.cap = cv2.VideoCapture(r"" + self.video_path)
                self.name = self.video_path.split('/')[-1]
                # print(self.name)

                self.fps = self.cap.get(cv2.CAP_PROP_FPS)
                self.width, self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
                    self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                out = cv2.VideoWriter('./Flask_Http-File/translate_file/{}'.format(self.save_name), self.fourcc,
                                      self.fps,
                                      (self.width, self.height))
            elif self.changeFlag == 1 and self.capture == 1:
                self.changeFlag = 0
                self.cap = cv2.VideoCapture(0)

                self.fps = self.cap.get(cv2.CAP_PROP_FPS)
                self.width, self.height = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH)), int(
                    self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                out = cv2.VideoWriter('./Flask_Http-File/translate_file/capture_result.mp4', self.fourcc, self.fps,
                                      (self.width, self.height))

            if self.video_path != "" or self.capture == 1:
                if self.cap.isOpened():
                    ret, frame = self.cap.read()
                    '''
                        对frame进行操作
                    '''
                    frame = frame  # 暂用进行测试
                    out.write(frame)
                    time.sleep(0.04)  # 控制读取录像的时间，后续可更改，但是为了防止进程混乱建议加上

                    # # 控制循环播放，不需要可以删除
                    if frame is None:
                        out.release()
                    #     self.cap = cv2.VideoCapture(r"" + self.video_path)

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

        fileName, fileType = QFileDialog.getOpenFileName(
            self, "选取文件", "./", "Excel Files (*.mp4);;Excel Files (*.avi)")

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
                    self.playLabel.setPixmap(
                        QPixmap.fromImage(qimg))  # 图像在QLabel上展示
            time.sleep(0.001)


class socketMessage(QThread):
    def __init__(self):
        super(socketMessage, self).__init__()
        self.threadFlag = 0  # 控制线程退出
        self.Received = 0
        self.socket_server = socket(AF_INET, SOCK_STREAM)
        self.socket_server.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        self.socket_server.bind(ADDR)
        self.name = ''
        self.style = 1
        self.filename = ''

    def run(self):
        self.socket_server.listen()
        conn, addr = self.socket_server.accept()
        while (self.isRunning()):
            ret = json.loads(conn.recv(BUFIZ))
            self.Received = 1
            # handle the message
            result = self.socketHandle(ret)

            print("name= " + self.name)
            print("filename= " + self.filename)
            print("style= {}".format(self.style))

            time.sleep(0.04)

        print("Socket disconnect")
        conn.close()
        # wait for update
        self.socket_server.close()

    def socketHandle(self, ret):
        self.name = ret['NAME']
        self.filename = ret['FILENAME']
        self.style = ret['STYLE']
        return 1
