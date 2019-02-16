from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QDesktopWidget,QMainWindow
import sys
import os
import sqlite3
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.setEnabled(True)
        MainWindow.resize(1280, 720)
        MainWindow.setWindowTitle('招聘信息提取分析器')
        MainWindow.setWindowIcon(QtGui.QIcon(os.getcwd() + '/resource/myico.png'))      

        #set mainwindow to center of desktop
        qr = MainWindow.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        MainWindow.move(qr.topLeft())

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)

        qss_file = open(os.getcwd() + '/resource/QSS/Mainwindow.qss').read()
        self.setStyleSheet(qss_file)

        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        

        self.TypeBox = QtWidgets.QComboBox(self.centralwidget)
        self.TypeBox.setGeometry(QtCore.QRect(20, 40, 100, 28))

        self.positionEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.positionEdit.setGeometry(QtCore.QRect(170, 40, 170, 30))
        self.positionEdit.setObjectName("postionEdit")
    
        self.keywordEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.keywordEdit.setGeometry(QtCore.QRect(430, 40, 260, 30))
        self.keywordEdit.setObjectName("keywordEdit")

        self.serchBtn = QtWidgets.QPushButton(self.centralwidget)
        self.serchBtn.setGeometry(QtCore.QRect(970, 40, 300, 30))
        self.serchBtn.setObjectName("serchBtn")
        self.serchBtn.clicked.connect(self.work)

        self.SalaryImage = QtWidgets.QLabel(self.centralwidget)
        self.SalaryImage.setGeometry(QtCore.QRect(520, 80, 440, 600))
        self.SalaryImage.setAlignment(QtCore.Qt.AlignCenter)
        self.SalaryImage.setObjectName("SalaryImage")
        
        self.PositionImage = QtWidgets.QLabel(self.centralwidget)
        self.PositionImage.setGeometry(QtCore.QRect(20, 80, 500, 600))
        self.PositionImage.setAlignment(QtCore.Qt.AlignCenter)
        self.PositionImage.setObjectName("PositionImage")

        #从数据库里得到最后一次搜索的网站类型，便于恢复数据显示
        

        self.TypeLabel = QtWidgets.QLabel(self.centralwidget)
        self.TypeLabel.setGeometry(QtCore.QRect(20,5,100,35))
        self.TypeLabel.setObjectName("TypeLabel")
      
        self.PositionLabel = QtWidgets.QLabel(self.centralwidget)
        self.PositionLabel.setGeometry(QtCore.QRect(180, 8, 250, 35))
        self.PositionLabel.setObjectName("PostionLabel")

        self.KeywordLabel = QtWidgets.QLabel(self.centralwidget)
        self.KeywordLabel.setGeometry(QtCore.QRect(425, 8, 330, 30))
        self.KeywordLabel.setObjectName("KeywordLabel")

        self.Crawl_label = QtWidgets.QLabel(self.centralwidget)
        self.Crawl_label.setGeometry(QtCore.QRect(750, 5, 170, 35))
        self.Crawl_label.setObjectName("label")

        self.listWidget = QtWidgets.QListWidget(self.centralwidget)
        self.listWidget.setGeometry(QtCore.QRect(970, 80, 300, 600))
        self.listWidget.setObjectName("listWidget")
        self.listWidget.doubleClicked.connect(self.showItem)
        


        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBar.setGeometry(QtCore.QRect(970, 10, 300, 20))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName("progressBar")

        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(750, 40, 170, 30))
        self.spinBox.setObjectName("spinBox")
        self.spinBox.setValue(20)
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(100)

        #设置菜单栏
        exitAction = QtWidgets.QAction(QtGui.QIcon(os.getcwd() + '/resource/myico.png'),'退出',self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.triggered.connect(QtWidgets.qApp.quit)

        aboutAction = QtWidgets.QAction(QtGui.QIcon(os.getcwd() + '/resource/myico.png'),'关于 Qt',self)
        aboutAction.triggered.connect(QtWidgets.qApp.aboutQt)

        outPutAction = QtWidgets.QAction(QtGui.QIcon(os.getcwd() + '/resource/myico.png'),'导出文件',self)
        outPutAction.triggered.connect(self.outPutFile)

        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1280, 28))
        self.menubar.setObjectName("menubar")

        fileMenu = self.menubar.addMenu('&文件')
        fileMenu.addAction(exitAction)

        aboutMenu = self.menubar.addMenu('&关于')
        aboutMenu.addAction(aboutAction)

        outPutMenu = self.menubar.addMenu('&导出文件')
        outPutMenu.addAction(outPutAction)
        


        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")

        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #界面初始化时，读取一次文件并存入内存中，方便提取
        

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "招聘信息抓取分析器"))
        self.serchBtn.setText(_translate("MainWindow", "搜索"))
        self.PositionLabel.setText(_translate("MainWindow", "位置 （例如 郑州）:"))
        self.KeywordLabel.setText(_translate("MainWindow", "关键字（例如 python）:"))
        self.Crawl_label.setText(_translate("MainWindow", "爬取的网页数: "))
        self.TypeLabel.setText(_translate("MainWindow", "选择爬取网站: "))
        self.TypeBox.addItem("拉勾网")
        self.TypeBox.addItem("智联招聘")

    def outPutFile(self):
        self.Filedialog = QtWidgets.QDialog(self.centralwidget)
        self.Filedialog.setFixedSize(600,150)
        self.Filedialog.setWindowTitle('导出EXCEL文件')
        self.Filedialog.setModal(True)
        

        self.Dirlabel = QtWidgets.QLabel(self.Filedialog)
        self.Dirlabel.move(20,40)
        self.Dirlabel.setFixedSize(70,30)
        self.Dirlabel.setText('文件位置: ')

        self.DirlineEdit = QtWidgets.QLineEdit(self.Filedialog)
        self.DirlineEdit.move(100,40)
        self.DirlineEdit.setFixedSize(350,30)
        self.DirlineEdit.setText(os.getcwd())

        self.Filelabel = QtWidgets.QLabel(self.Filedialog)
        self.Filelabel.move(20,100)
        self.Filelabel.setFixedSize(70,30)
        self.Filelabel.setText('文件名称: ')

        self.FilelineEdit = QtWidgets.QLineEdit(self.Filedialog)
        self.FilelineEdit.move(100,100)
        self.FilelineEdit.setFixedSize(350,30)

        self.YesButton = QtWidgets.QPushButton(self.Filedialog)
        self.YesButton.move(470,100)
        self.YesButton.setFixedSize(100,30)
        self.YesButton.setText('确定')
        self.YesButton.clicked.connect(self.saveFileToExcel)

        self.browlButton = QtWidgets.QPushButton(self.Filedialog)
        self.browlButton.move(470,40)
        self.browlButton.setFixedSize(100,30)
        self.browlButton.setText('浏览')
        self.browlButton.clicked.connect(self.openFile)

        self.Filedialog.show()



    





        
















