import sys
from typing import Any
import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from ultralytics import YOLO,settings
from ModleDetect import objectDetect
import sqlite3


class Boycott:
    def __init__(self, model_name):
        self.app = QtWidgets.QApplication(sys.argv)
        self.window = QtWidgets.QWidget()
        self.camera = cv2.VideoCapture(0)
        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 620)
        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.label = QtWidgets.QLabel(self.window)
        self.label.setGeometry(150, 50, 800, 600)
        self.label.setScaledContents(True)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.detector = objectDetect(model_name)
        self.start = False
        self.conn = sqlite3.connect('image.db')
        self.cursor = self.conn.cursor()
        create_table_query = '''
                              CREATE TABLE IF NOT EXISTS oimage(
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                path TEXT NOT NULL
                              )'''
        self.cursor.execute(create_table_query)
        self.conn.commit()

        self.cursor.execute('''
                            CREATE TABLE IF NOT EXISTS dimage
                              (id INTEGER PRIMARY KEY AUTOINCREMENT,
                               path TEXT NOT NULL,
                               originalpath TEXT NOT NULL
                              )''')
        self.conn.commit()

    def update_frame(self):
        if self.start:
            ret, frame = self.camera.read()
            if ret:
                annotated_frame = self.detector.web_cam(frame)
                frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                image = QtGui.QImage(frame_rgb.data, frame_rgb.shape[1], frame_rgb.shape[0], QtGui.QImage.Format_RGB888)
                pixmap = QtGui.QPixmap.fromImage(image)
                self.label.setPixmap(pixmap)

    def open_image(self):
        file_dialog = QtWidgets.QFileDialog()
        file_path, _ = file_dialog.getOpenFileName(self.window, "فتح ملف الصورة", "", "صور (*.png *.jpg *.jpeg)")
        if file_path:
            self.image_path = file_path  # Store the image path
            detect_image, path, accuracy = self.detector.imageDetect(self.image_path)

            full_path_detect_image = f"{path}/{detect_image}"
            insert_query = "INSERT INTO oimage (path) VALUES (?)"
            self.cursor.execute(insert_query, (self.image_path,))
            self.cursor.execute("INSERT INTO dimage (path, originalpath) VALUES (?, ?)", (full_path_detect_image, self.image_path,))
            self.conn.commit()

            print(full_path_detect_image)

            image = QtGui.QImage(full_path_detect_image)

            if image.isNull():
                QtWidgets.QMessageBox.warning(self.window, "خطأ", "تعذر فتح ملف الصورة!")
            else:
                self.label.setPixmap(QtGui.QPixmap.fromImage(image))

            # Check if the accuracy is higher than 0.9
            if accuracy > 0.9:
                QtWidgets.QMessageBox.information(self.window, "تحذير", "The product is boycutt!")

    def start_camera(self):
        self.timer.start(30)
        self.start=True

    def stop_camera(self):
        self.timer.stop()
        self.start=False


    '''  
    this function of interface
    
    '''
    def Windows_program(self):
        self.window.resize(600, 400)
        self.window.setWindowTitle('Boycott Products')
        self.window.setWindowIcon(QtGui.QIcon("imgs/Boy-pro.jpg"))
        self.window.show()
        self.app.exec_()

    def Label(self):
        lbl = QtWidgets.QLabel('<h1>Get to know the boycott products</h1>', self.window)
        lbl.setStyleSheet(" background-color: #198754;")
        lbl.move(100, 20)
        image = QtGui.QImage('img_boycott/Boycott-logo.png3_.jpg')
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
        self.label.setGeometry(150, 50, 400, 300)
        self.label.setScaledContents(True)


    
    def Button1(self):
        btn1 = QtWidgets.QPushButton('Show Photo', self.window)
        btn1.setGeometry(30, 70, 100, 50)
        btn1.setStyleSheet("color: #fff;background-color: #0b5ed7;border-color: #0a58ca;font-size:13px")
        btn1.setIcon(QtGui.QIcon("imgs/files.png"))
        btn1.clicked.connect(self.open_image)

    def Button2(self):
        btn2 = QtWidgets.QPushButton("start Camera", self.window)
        btn2.setGeometry(30, 130, 100, 50)
        btn2.setStyleSheet("color: #fff;background-color: #0b5ed7;border-color: #0a58ca;font-size:13px")
        btn2.setIcon(QtGui.QIcon("imgs/camera.png"))
        btn2.clicked.connect(self.start_camera)

    def Button3(self):
        btn3 = QtWidgets.QPushButton("stope Camera", self.window)
        btn3.setGeometry(30, 190, 100, 50)
        btn3.setStyleSheet("color: #fff;background-color: #0b5ed7;border-color: #0a58ca;font-size:13px")
        btn3.setIcon(QtGui.QIcon("imgs/clos-camera.png"))
        btn3.clicked.connect(self.stop_camera)

    def Button4(self):
        btn4 = QtWidgets.QPushButton("EXIT", self.window)
        btn4.setGeometry(30, 250, 100, 50)
        btn4.setStyleSheet("color: #fff;background-color: #AC1010;border-color: #0a58ca;font-size:13px")
        btn4.setIcon(QtGui.QIcon("imgs/Untitled.png"))
        btn4.clicked.connect(exit)

    def show(self):
        self.Label()
        self.Button1()
        self.Button2()
        self.Button3()
        self.Button4()
        self.Windows_program()

model_name = 'best.pt'
show = Boycott(model_name)

show.show()
