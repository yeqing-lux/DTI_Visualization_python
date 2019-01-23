# -*- coding: utf-8 -*-
import math
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QColorDialog
from vtk.qt.QVTKRenderWindowInteractor import QVTKRenderWindowInteractor
from util import *


class Ui_MainWindow(object):
    def __init__(self):
        self.line_data = None

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1015, 712)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.widget_1 = QtWidgets.QWidget(self.centralwidget)
        self.widget_1.setGeometry(QtCore.QRect(20, 20, 341, 311))
        self.widget_1.setObjectName("widget_1")
        self.line_5 = QtWidgets.QFrame(self.widget_1)
        self.line_5.setGeometry(QtCore.QRect(-10, -20, 721, 21))
        self.line_5.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_5.setObjectName("line_5")
        self.widget_3 = QtWidgets.QWidget(self.centralwidget)
        self.widget_3.setGeometry(QtCore.QRect(20, 350, 341, 311))
        self.widget_3.setObjectName("widget_3")
        self.widget_2 = QtWidgets.QWidget(self.centralwidget)
        self.widget_2.setGeometry(QtCore.QRect(380, 20, 341, 311))
        self.widget_2.setObjectName("widget_2")
        self.widget_4 = QtWidgets.QWidget(self.centralwidget)
        self.widget_4.setGeometry(QtCore.QRect(380, 350, 341, 311))
        self.widget_4.setObjectName("widget_4")

        self.line = QtWidgets.QFrame(self.centralwidget)
        self.line.setGeometry(QtCore.QRect(10, 330, 721, 21))
        self.line.setFrameShape(QtWidgets.QFrame.HLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.line_2 = QtWidgets.QFrame(self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(360, 10, 20, 661))
        self.line_2.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_2.setObjectName("line_2")
        self.line_3 = QtWidgets.QFrame(self.centralwidget)
        self.line_3.setGeometry(QtCore.QRect(720, 10, 20, 661))
        self.line_3.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.line_4 = QtWidgets.QFrame(self.centralwidget)
        self.line_4.setGeometry(QtCore.QRect(0, 10, 20, 661))
        self.line_4.setFrameShape(QtWidgets.QFrame.VLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.line_6 = QtWidgets.QFrame(self.centralwidget)
        self.line_6.setGeometry(QtCore.QRect(10, 0, 721, 21))
        self.line_6.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_6.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_6.setObjectName("line_6")
        self.line_7 = QtWidgets.QFrame(self.centralwidget)
        self.line_7.setGeometry(QtCore.QRect(10, 660, 721, 21))
        self.line_7.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_7.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_7.setObjectName("line_7")
        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(740, 10, 261, 201))
        self.listWidget.setObjectName("listWidget")
        self.listWidget_2 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_2.setGeometry(QtCore.QRect(740, 240, 261, 201))
        self.listWidget_2.setObjectName("listWidget_2")
        self.line_8 = QtWidgets.QFrame(self.centralwidget)
        self.line_8.setGeometry(QtCore.QRect(740, 220, 251, 16))
        self.line_8.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_8.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_8.setObjectName("line_8")
        self.line_9 = QtWidgets.QFrame(self.centralwidget)
        self.line_9.setGeometry(QtCore.QRect(740, 440, 251, 21))
        self.line_9.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_9.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_9.setObjectName("line_9")
        self.listWidget_3 = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget_3.setGeometry(QtCore.QRect(740, 461, 261, 201))
        self.listWidget_3.setObjectName("listWidget_3")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(840, 20, 81, 16))
        self.label.setObjectName("label")
        self.line_10 = QtWidgets.QFrame(self.centralwidget)
        self.line_10.setGeometry(QtCore.QRect(740, 40, 261, 16))
        self.line_10.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_10.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_10.setObjectName("line_10")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(750, 100, 121, 41))
        self.pushButton.setObjectName("pushButton")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(750, 70, 51, 16))
        self.label_2.setObjectName("label_2")
        self.comboBox = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox.setGeometry(QtCore.QRect(800, 50, 71, 51))
        self.comboBox.setObjectName("comboBox")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(890, 70, 21, 16))
        self.label_3.setObjectName("label_3")
        self.comboBox_2 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_2.setGeometry(QtCore.QRect(920, 50, 71, 51))
        self.comboBox_2.setObjectName("comboBox_2")
        self.lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEdit.setGeometry(QtCore.QRect(760, 150, 231, 41))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(870, 100, 121, 41))
        self.pushButton_2.setObjectName("pushButton_2")

        # self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        # self.progressBar.setGeometry(QtCore.QRect(760, 170, 221, 23))
        # self.progressBar.setProperty("value", 24)
        # self.progressBar.setObjectName("progressBar")
        # self.timer = QBasicTimer()
        # self.step = 0
        # self.progressBar.setValue(0)

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(800, 250, 151, 16))
        self.label_4.setObjectName("label_4")
        self.line_11 = QtWidgets.QFrame(self.centralwidget)
        self.line_11.setGeometry(QtCore.QRect(740, 270, 261, 16))
        self.line_11.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_11.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_11.setObjectName("line_11")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(750, 300, 81, 16))
        self.label_5.setObjectName("label_5")
        self.horizontalSlider = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider.setGeometry(QtCore.QRect(850, 291, 131, 31))
        self.horizontalSlider.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider.setObjectName("horizontalSlider")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(750, 330, 81, 16))
        self.label_6.setObjectName("label_6")
        self.horizontalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.horizontalSlider_2.setGeometry(QtCore.QRect(850, 320, 131, 31))
        self.horizontalSlider_2.setOrientation(QtCore.Qt.Horizontal)
        self.horizontalSlider_2.setObjectName("horizontalSlider_2")
        self.label_7 = QtWidgets.QLabel(self.centralwidget)
        self.label_7.setGeometry(QtCore.QRect(750, 370, 101, 16))
        self.label_7.setObjectName("label_7")
        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(850, 360, 71, 41))
        self.pushButton_3.setObjectName("pushButton_3")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(940, 360, 41, 41))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_8 = QtWidgets.QLabel(self.centralwidget)
        self.label_8.setGeometry(QtCore.QRect(750, 410, 61, 16))
        self.label_8.setObjectName("label_8")
        self.pushButton_4 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_4.setGeometry(QtCore.QRect(850, 400, 71, 31))
        self.pushButton_4.setObjectName("pushButton_4")
        self.label_9 = QtWidgets.QLabel(self.centralwidget)
        self.label_9.setGeometry(QtCore.QRect(860, 470, 31, 16))
        self.label_9.setObjectName("label_9")
        self.line_12 = QtWidgets.QFrame(self.centralwidget)
        self.line_12.setGeometry(QtCore.QRect(740, 490, 261, 16))
        self.line_12.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_12.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_12.setObjectName("line_12")
        self.label_10 = QtWidgets.QLabel(self.centralwidget)
        self.label_10.setGeometry(QtCore.QRect(760, 520, 91, 16))
        self.label_10.setObjectName("label_10")
        self.comboBox_3 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_3.setGeometry(QtCore.QRect(860, 500, 71, 51))
        self.comboBox_3.setObjectName("comboBox_3")
        self.label_11 = QtWidgets.QLabel(self.centralwidget)
        self.label_11.setGeometry(QtCore.QRect(760, 550, 120, 16))
        self.label_11.setObjectName("label_11")

        self.label_12 = QtWidgets.QLabel(self.centralwidget)
        self.label_12.setGeometry(QtCore.QRect(760, 590, 10, 16))
        self.label_12.setObjectName("label_12")
        self.comboBox_4 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_4.setGeometry(QtCore.QRect(775, 580, 60, 30))
        self.comboBox_4.setObjectName("comboBox_4")
        self.label_13 = QtWidgets.QLabel(self.centralwidget)
        self.label_13.setGeometry(QtCore.QRect(840, 590, 10, 16))
        self.label_13.setObjectName("label_13")
        self.comboBox_5 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_5.setGeometry(QtCore.QRect(855, 580, 60, 30))
        self.comboBox_5.setObjectName("comboBox_5")
        self.label_14 = QtWidgets.QLabel(self.centralwidget)
        self.label_14.setGeometry(QtCore.QRect(920, 590, 10, 16))
        self.label_14.setObjectName("label_14")
        self.comboBox_6 = QtWidgets.QComboBox(self.centralwidget)
        self.comboBox_6.setGeometry(QtCore.QRect(930, 580, 60, 30))
        self.comboBox_6.setObjectName("comboBox_6")

        self.pushButton_8 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_8.setGeometry(QtCore.QRect(760, 620, 101, 31))
        self.pushButton_8.setObjectName("pushButton_8")
        self.pushButton_9 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_9.setGeometry(QtCore.QRect(870, 620, 101, 31))
        self.pushButton_9.setObjectName("pushButton_9")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1015, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        ####comboBox
        self.comboBox.addItem("10")
        self.comboBox.addItem("20")
        self.comboBox.addItem("30")
        self.comboBox.addItem("40")
        self.comboBox.addItem("50")
        self.comboBox.addItem("60")
        self.comboBox.addItem("70")
        self.comboBox.addItem("80")
        self.comboBox.setCurrentIndex(5)

        self.comboBox_2.addItem("0.1")
        self.comboBox_2.addItem("0.2")
        self.comboBox_2.addItem("0.3")
        self.comboBox_2.addItem("0.4")
        self.comboBox_2.addItem("0.5")
        self.comboBox_2.addItem("0.6")
        self.comboBox_2.addItem("0.7")
        self.comboBox_2.addItem("0.8")
        self.comboBox_2.addItem("0.9")
        self.comboBox_2.setCurrentIndex(2)

        self.comboBox_3.addItem("1")
        self.comboBox_3.addItem("2")
        self.comboBox_3.addItem("3")

        for i in range(30, 130 + 1):
            self.comboBox_4.addItem(str(i))
            self.comboBox_5.addItem(str(i))
            self.comboBox_6.addItem(str(i))

        #### VTK
        self.vtkWidget4 = QVTKRenderWindowInteractor(self.widget_4)
        self.ren4 = vtk.vtkRenderer()
        self.vtkWidget4.GetRenderWindow().AddRenderer(self.ren4)
        self.iren4 = self.vtkWidget4.GetRenderWindow().GetInteractor()
        self.vtkWidget1 = QVTKRenderWindowInteractor(self.widget_1)
        self.vtkWidget2 = QVTKRenderWindowInteractor(self.widget_2)
        self.vtkWidget3 = QVTKRenderWindowInteractor(self.widget_3)
        self.ren1 = vtk.vtkRenderer()
        self.ren2 = vtk.vtkRenderer()
        self.ren3 = vtk.vtkRenderer()

        self.vtkWidget1.GetRenderWindow().AddRenderer(self.ren1)
        self.vtkWidget2.GetRenderWindow().AddRenderer(self.ren2)
        self.vtkWidget3.GetRenderWindow().AddRenderer(self.ren3)
        self.iren1 = self.vtkWidget1.GetRenderWindow().GetInteractor()
        self.iren2 = self.vtkWidget2.GetRenderWindow().GetInteractor()
        self.iren3 = self.vtkWidget3.GetRenderWindow().GetInteractor()
        self.vtkWidget4.SetInteractorStyle(vtk.vtkInteractorStyleTrackballCamera())

        #### 修改的部分
        self.interactorStyle1 = vtk.vtkInteractorStyleImage()
        self.vtkWidget1.SetInteractorStyle(self.interactorStyle1)
        self.interactorStyle2 = vtk.vtkInteractorStyleImage()
        self.vtkWidget2.SetInteractorStyle(self.interactorStyle2)
        self.interactorStyle3 = vtk.vtkInteractorStyleImage()
        self.vtkWidget3.SetInteractorStyle(self.interactorStyle3)

        #### BUTTON
        self.pushButton.clicked.connect(self.select_file)
        self.pushButton_2.clicked.connect(self.running)
        self.pushButton_3.clicked.connect(self.showDialog)
        self.pushButton_4.clicked.connect(self.reset)
        self.pushButton_8.clicked.connect(self.generate_ROI)
        self.pushButton_9.clicked.connect(self.reset)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #### Slide
        self.horizontalSlider.setValue(50)
        self.horizontalSlider_2.setValue(50)
        self.horizontalSlider.valueChanged[int].connect(self.changeValue)
        self.horizontalSlider_2.valueChanged[int].connect(self.changeValue_2)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "INITIALIZE"))
        self.pushButton.setText(_translate("MainWindow", "SELECT FILE"))
        self.label_2.setText(_translate("MainWindow", "THETA "))
        self.label_3.setText(_translate("MainWindow", "FA"))
        self.pushButton_2.setText(_translate("MainWindow", "CONFIRM"))
        self.label_4.setText(_translate("MainWindow", "PARAMETER SETTINGS"))
        self.label_5.setText(_translate("MainWindow", "BRIGTHNESS"))
        self.label_6.setText(_translate("MainWindow", "CONTRAST"))
        self.label_7.setText(_translate("MainWindow", "SINGLE COLOR"))
        self.pushButton_3.setText(_translate("MainWindow", " PANE"))
        self.label_8.setText(_translate("MainWindow", "RESET"))
        self.pushButton_4.setText(_translate("MainWindow", "YES"))
        self.label_9.setText(_translate("MainWindow", "ROI"))
        self.label_10.setText(_translate("MainWindow", "SELECT PANE"))
        self.label_11.setText(_translate("MainWindow", "SELECT LOCATION"))
        self.label_12.setText(_translate("MainWindow", "X"))
        self.label_13.setText(_translate("MainWindow", "Y"))
        self.label_14.setText(_translate("MainWindow", "Z"))
        self.pushButton_8.setText(_translate("MainWindow", "CONFIRM"))
        self.pushButton_9.setText(_translate("MainWindow", "CANCEL"))

    def select_file(self):
        """
        Select NIfTI file from user's computer.
        """
        path, others = QFileDialog.getOpenFileName(self.centralwidget, caption='Open file', directory='/')
        self.lineEdit.setText(path)
        # self.lineEdit.adjustSize()

    def running(self):
        #### VTK
        file_name = self.lineEdit.text()
        # self.line_data = read(file_name, cos=math.cos(int(self.comboBox.currentText()) * math.pi / 180),
        #                       FA=float(self.comboBox_2.currentText()))
        self.line_data = load_pickle("/Users/yeqing/Desktop/课程/DTI/line_data.pkl")
        createLine(self.ren4, line_data=self.line_data)
        self.vtkWidget4.GetRenderWindow().Render()

        ##调用全局函数
        # slice(self.ren1, self.vtkWidget1.GetRenderWindow(), self.vtkWidget1, self.interactorStyle1, 0,
        #       img1=nib.load(file_name))
        # slice(self.ren2, self.vtkWidget2.GetRenderWindow(), self.vtkWidget2, self.interactorStyle2, 1,
        #       img1=nib.load(file_name))
        # slice(self.ren3, self.vtkWidget3.GetRenderWindow(), self.vtkWidget3, self.interactorStyle3, 2,
        #       img1=nib.load(file_name))
        # self.vtkWidget1.GetRenderWindow().Render()
        # self.vtkWidget2.GetRenderWindow().Render()
        # self.vtkWidget3.GetRenderWindow().Render()
        self.vtkWidget4.GetRenderWindow().Render()

        self.iren4.Initialize()
        # self.iren1.Initialize()
        # self.iren2.Initialize()
        # self.iren3.Initialize()

    def running1(self):
        """
        Running FACT algorithm.
        """
        # VTK
        file_name = self.lineEdit.text()
        self.line_data = read(file_name, cos=math.cos(int(self.comboBox.currentText()) * math.pi / 180),
                              FA=float(self.comboBox_2.currentText()))
        createLine(self.ren4, line_data=self.line_data)
        self.vtkWidget4.GetRenderWindow().Render()

        # 调用全局函数
        slice(self.ren1, self.vtkWidget1.GetRenderWindow(), self.vtkWidget1, self.interactorStyle1, 0,
              img1=nib.load(file_name))
        slice(self.ren2, self.vtkWidget2.GetRenderWindow(), self.vtkWidget2, self.interactorStyle2, 1,
              img1=nib.load(file_name))
        slice(self.ren3, self.vtkWidget3.GetRenderWindow(), self.vtkWidget3, self.interactorStyle3, 2,
              img1=nib.load(file_name))
        self.vtkWidget1.GetRenderWindow().Render()
        self.vtkWidget2.GetRenderWindow().Render()
        self.vtkWidget3.GetRenderWindow().Render()
        self.vtkWidget4.GetRenderWindow().Render()

        self.iren4.Initialize()
        self.iren1.Initialize()
        self.iren2.Initialize()
        self.iren3.Initialize()

    def changeValue(self, value):
        """
        Change the value of brightness, i.e. a.
        """
        createLine(self.ren4, a=1.0 + value * 0.01, line_data=self.line_data)
        self.vtkWidget4.GetRenderWindow().Render()

    def changeValue_2(self, value):
        """
        Change the value of contrast, i.e. b.
        """
        createLine(self.ren4, b=10 + value, line_data=self.line_data)
        self.vtkWidget4.GetRenderWindow().Render()

    def showDialog(self):
        """
        Show the color pane button.
        """
        col = QColorDialog.getColor()

        if col.isValid():
            self.frame.setStyleSheet("QWidget { background-color: %s }"
                                     % col.name())
            h = str(col.name())[1:]
            color = tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))
            createLine(self.ren4, line_color=color, line_data=self.line_data)
            self.vtkWidget4.GetRenderWindow().Render()

    def reset(self):
        """
        Reset color settings.
        """
        self.horizontalSlider.setValue(50)
        self.horizontalSlider_2.setValue(50)
        self.ren4 = vtk.vtkRenderer()
        self.vtkWidget4.GetRenderWindow().AddRenderer(self.ren4)

        createLine(self.ren4, a=1.5, b=60, line_data=self.line_data, circle_actor=None)
        self.vtkWidget4.GetRenderWindow().Render()

    def generate_ROI(self):
        """
        Generate ROI result.
        """
        indicator = int(self.comboBox_3.currentText()) - 1
        X = int(self.comboBox_4.currentText())
        Y = int(self.comboBox_5.currentText())
        Z = int(self.comboBox_6.currentText())
        self.ren4 = vtk.vtkRenderer()
        self.vtkWidget4.GetRenderWindow().AddRenderer(self.ren4)
        ROIdata = ROIsearch(self.line_data, (X, Y, Z), indicator=indicator, r=20)
        circle_actor = ROI_circlePolyData((X, Y, Z), indicator=indicator, r=20)
        createLine(self.ren4, a=1.5, b=60, line_data=ROIdata, circle_actor=circle_actor)
        self.vtkWidget4.GetRenderWindow().Render()


