#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# STDF Fixer
# Author: noonchen @ Github
# Email: chennoon233@gmail.com
# License: GPL-3.0

import os
import sys
import threading
from datetime import datetime
from stdfFixer import stdfFixer
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog


class UI_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(355, 589)
        MainWindow.setMinimumSize(QtCore.QSize(355, 589))
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setMinimumSize(QtCore.QSize(0, 0))
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(10, 10, 10, 0)
        self.verticalLayout_2.setSpacing(5)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.MessageGroup = QtWidgets.QGroupBox(self.centralwidget)
        self.MessageGroup.setObjectName("MessageGroup")
        self.gridLayout = QtWidgets.QGridLayout(self.MessageGroup)
        self.gridLayout.setContentsMargins(10, 5, 10, 10)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.MessageBox = QtWidgets.QTextBrowser(self.MessageGroup)
        font = QtGui.QFont()
        font.setFamily("Courier New")
        font.setPointSize(10)
        self.MessageBox.setFont(font)
        self.MessageBox.setObjectName("MessageBox")
        self.gridLayout.addWidget(self.MessageBox, 0, 0, 1, 1)
        self.verticalLayout_2.addWidget(self.MessageGroup)
        self.horizontalLayout_bar = QtWidgets.QHBoxLayout()
        self.horizontalLayout_bar.setContentsMargins(10, 5, 10, -1)
        self.horizontalLayout_bar.setSpacing(0)
        self.horizontalLayout_bar.setObjectName("horizontalLayout_bar")
        self.progressBar = QtWidgets.QProgressBar(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setItalic(True)
        self.progressBar.setFont(font)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setInvertedAppearance(False)
        self.progressBar.setObjectName("progressBar")
        self.horizontalLayout_bar.addWidget(self.progressBar)
        self.verticalLayout_2.addLayout(self.horizontalLayout_bar)
        self.PathGroup = QtWidgets.QGroupBox(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PathGroup.sizePolicy().hasHeightForWidth())
        self.PathGroup.setSizePolicy(sizePolicy)
        self.PathGroup.setObjectName("PathGroup")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.PathGroup)
        self.verticalLayout.setContentsMargins(10, 5, 10, 10)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_stdinput = QtWidgets.QHBoxLayout()
        self.horizontalLayout_stdinput.setSpacing(0)
        self.horizontalLayout_stdinput.setObjectName("horizontalLayout_stdinput")
        self.line_std_input = QtWidgets.QPlainTextEdit(self.PathGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_std_input.sizePolicy().hasHeightForWidth())
        self.line_std_input.setSizePolicy(sizePolicy)
        self.line_std_input.setMinimumSize(QtCore.QSize(0, 41))
        self.line_std_input.setMaximumSize(QtCore.QSize(16777215, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.line_std_input.setFont(font)
        self.line_std_input.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.line_std_input.setObjectName("line_std_input")
        self.horizontalLayout_stdinput.addWidget(self.line_std_input)
        self.button_openTmp = QtWidgets.QToolButton(self.PathGroup)
        self.button_openTmp.setMinimumSize(QtCore.QSize(31, 41))
        self.button_openTmp.setMaximumSize(QtCore.QSize(31, 41))
        self.button_openTmp.setIconSize(QtCore.QSize(20, 20))
        self.button_openTmp.setObjectName("button_openTmp")
        self.horizontalLayout_stdinput.addWidget(self.button_openTmp)
        self.verticalLayout.addLayout(self.horizontalLayout_stdinput)
        self.horizontalLayout_stdoutput = QtWidgets.QHBoxLayout()
        self.horizontalLayout_stdoutput.setSpacing(0)
        self.horizontalLayout_stdoutput.setObjectName("horizontalLayout_stdoutput")
        self.line_std_output = QtWidgets.QPlainTextEdit(self.PathGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_std_output.sizePolicy().hasHeightForWidth())
        self.line_std_output.setSizePolicy(sizePolicy)
        self.line_std_output.setMinimumSize(QtCore.QSize(0, 41))
        self.line_std_output.setMaximumSize(QtCore.QSize(16777215, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.line_std_output.setFont(font)
        self.line_std_output.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.line_std_output.setObjectName("line_std_output")
        self.horizontalLayout_stdoutput.addWidget(self.line_std_output)
        self.button_openFolder = QtWidgets.QToolButton(self.PathGroup)
        self.button_openFolder.setMinimumSize(QtCore.QSize(31, 41))
        self.button_openFolder.setMaximumSize(QtCore.QSize(31, 41))
        self.button_openFolder.setIconSize(QtCore.QSize(20, 20))
        self.button_openFolder.setObjectName("button_openFolder")
        self.horizontalLayout_stdoutput.addWidget(self.button_openFolder)
        self.verticalLayout.addLayout(self.horizontalLayout_stdoutput)
        self.horizontalLayout_BDinput = QtWidgets.QHBoxLayout()
        self.horizontalLayout_BDinput.setSpacing(0)
        self.horizontalLayout_BDinput.setObjectName("horizontalLayout_BDinput")
        self.line_BD_input = QtWidgets.QPlainTextEdit(self.PathGroup)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.line_BD_input.sizePolicy().hasHeightForWidth())
        self.line_BD_input.setSizePolicy(sizePolicy)
        self.line_BD_input.setMinimumSize(QtCore.QSize(0, 41))
        self.line_BD_input.setMaximumSize(QtCore.QSize(16777215, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(8)
        font.setBold(True)
        font.setItalic(True)
        font.setWeight(75)
        self.line_BD_input.setFont(font)
        self.line_BD_input.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.line_BD_input.setObjectName("line_BD_input")
        self.horizontalLayout_BDinput.addWidget(self.line_BD_input)
        self.button_openBD = QtWidgets.QToolButton(self.PathGroup)
        self.button_openBD.setMinimumSize(QtCore.QSize(31, 41))
        self.button_openBD.setMaximumSize(QtCore.QSize(31, 41))
        self.button_openBD.setIconSize(QtCore.QSize(20, 20))
        self.button_openBD.setObjectName("button_openBD")
        self.horizontalLayout_BDinput.addWidget(self.button_openBD)
        self.verticalLayout.addLayout(self.horizontalLayout_BDinput)
        self.verticalLayout_2.addWidget(self.PathGroup)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(10, 5, 10, -1)
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.Use_BD = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(11)
        font.setBold(True)
        font.setWeight(75)
        self.Use_BD.setFont(font)
        self.Use_BD.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.Use_BD.setIconSize(QtCore.QSize(30, 30))
        self.Use_BD.setChecked(True)
        self.Use_BD.setTristate(False)
        self.Use_BD.setObjectName("Use_BD")
        self.horizontalLayout.addWidget(self.Use_BD)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.Start = QtWidgets.QPushButton(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.Start.sizePolicy().hasHeightForWidth())
        self.Start.setSizePolicy(sizePolicy)
        self.Start.setMinimumSize(QtCore.QSize(121, 41))
        self.Start.setMaximumSize(QtCore.QSize(121, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(True)
        font.setItalic(False)
        font.setWeight(75)
        self.Start.setFont(font)
        self.Start.setStyleSheet("border-radius: 5px;\n"
"background-color: rgb(0, 170, 0);\n"
"color: white;")
        self.Start.setDefault(False)
        self.Start.setFlat(False)
        self.Start.setObjectName("Start")
        self.horizontalLayout.addWidget(self.Start)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 355, 22))
        self.menubar.setObjectName("menubar")
        self.menuAbout = QtWidgets.QMenu(self.menubar)
        self.menuAbout.setObjectName("menuAbout")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionOpen_Bin_Definition_file = QtWidgets.QAction(MainWindow)
        self.actionOpen_Bin_Definition_file.setObjectName("actionOpen_Bin_Definition_file")
        self.actionSTD_tmp_file = QtWidgets.QAction(MainWindow)
        self.actionSTD_tmp_file.setObjectName("actionSTD_tmp_file")
        self.actionQuit = QtWidgets.QAction(MainWindow)
        self.actionQuit.setObjectName("actionQuit")
        self.actionAbout_STDF_Fixer = QtWidgets.QAction(MainWindow)
        self.actionAbout_STDF_Fixer.setObjectName("actionAbout_STDF_Fixer")
        self.actionBin_Definition = QtWidgets.QAction(MainWindow)
        self.actionBin_Definition.setObjectName("actionBin_Definition")
        self.actionHelp = QtWidgets.QAction(MainWindow)
        self.actionHelp.setObjectName("actionHelp")
        self.menuAbout.addAction(self.actionAbout_STDF_Fixer)
        self.menuAbout.addAction(self.actionHelp)
        self.menubar.addAction(self.menuAbout.menuAction())

        self.retranslateUi(MainWindow)
        self.Use_BD.clicked['bool'].connect(self.button_openBD.setEnabled)
        self.Use_BD.clicked['bool'].connect(self.line_BD_input.setEnabled)
        self.Use_BD.clicked['bool'].connect(self.line_BD_input.setVisible)
        self.Use_BD.clicked['bool'].connect(self.button_openBD.setVisible)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "STDF Fixer"))
        self.MessageGroup.setTitle(_translate("MainWindow", "Messages"))
        self.MessageBox.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'Courier New\'; font-size:10pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px; font-family:\'Courier New\';\"><br /></p></body></html>"))
        self.progressBar.setFormat(_translate("MainWindow", "%p%"))
        self.PathGroup.setTitle(_translate("MainWindow", "File Paths"))
        self.line_std_input.setPlaceholderText(_translate("MainWindow", "Select a broken or incomplete STDF file"))
        self.button_openTmp.setText(_translate("MainWindow", "..."))
        self.line_std_output.setPlaceholderText(_translate("MainWindow", "Select a folder to store the fixed STDF file"))
        self.button_openFolder.setText(_translate("MainWindow", "..."))
        self.line_BD_input.setToolTip(_translate("MainWindow", "The Bin Definition is used in NI TestStand that contains bin descriptions."))
        self.line_BD_input.setPlaceholderText(_translate("MainWindow", "Select the Bin Definition for the selected STDF file"))
        self.button_openBD.setText(_translate("MainWindow", "..."))
        self.Use_BD.setToolTip(_translate("MainWindow", "The Bin Definition is used in NI TestStand that contains bin descriptions."))
        self.Use_BD.setText(_translate("MainWindow", " Bin Definition\n"
" Available?"))
        self.Start.setText(_translate("MainWindow", "Start Fixing"))
        self.menuAbout.setTitle(_translate("MainWindow", "About"))
        self.actionOpen_Bin_Definition_file.setText(_translate("MainWindow", "Open Bin Definition file"))
        self.actionSTD_tmp_file.setText(_translate("MainWindow", "STD tmp file"))
        self.actionQuit.setText(_translate("MainWindow", "Quit"))
        self.actionAbout_STDF_Fixer.setText(_translate("MainWindow", "About STDF Fixer"))
        self.actionBin_Definition.setText(_translate("MainWindow", "Bin Definition"))
        self.actionHelp.setText(_translate("MainWindow", "Help"))


# high dpi stretch
if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
    QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
    QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)


class Signal(QtCore.QObject):
    # signal to update message box
    message_printer = QtCore.pyqtSignal(str)
    # signal to update progress bar
    pgbar_setter = QtCore.pyqtSignal(int)


class Fixer_UI(QMainWindow, UI_MainWindow):
    
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.Start.clicked.connect(self.startFix) # connect button to func
        self.button_openTmp.clicked.connect(self.stdInputDialog)
        self.button_openFolder.clicked.connect(self.outDirDialog)
        self.button_openBD.clicked.connect(self.BDInputDialog)
        self.actionAbout_STDF_Fixer.triggered.connect(self.showAbout)
        self.actionHelp.triggered.connect(self.showHelp)
        self.MessageBox.setOpenExternalLinks(True)
        
        self.custSignal = Signal()
        self.custSignal.message_printer.connect(self.update_message)
        self.custSignal.pgbar_setter.connect(self.update_pgbar)
        
        
    def update_message(self, text):
        self.MessageBox.append(text)
    
    def update_pgbar(self, num):
        self.progressBar.setValue(num)
        
        
    def stdInputDialog(self):
        fname, _typ = QFileDialog.getOpenFileName(None, 
                                             caption="Select STD File To Fix/Repair", 
                                             filter="STDF (*.std*);;All Files (*)", )
        if fname:
            self.line_std_input.setPlainText(fname)
            self.line_std_output.setPlainText(os.path.dirname(fname))
            
            
    def outDirDialog(self):
        outDir = QFileDialog.getExistingDirectory(None, 
                                                  caption="Select Directory To Save")
        if outDir:
            self.line_std_output.setPlainText(outDir)
    
    
    def BDInputDialog(self):
        fname, _typ = QFileDialog.getOpenFileName(None, 
                                             caption="Select Bin Definition", 
                                             filter="Bin Definition (*.bins);;All Files (*)", )
        if fname: self.line_BD_input.setPlainText(fname)
        
    
    def showHelp(self):
        self.custSignal.message_printer.emit('''<br>Refer to the <a href="https://github.com/noonchen/stdfFixer/blob/master/README.md">ReadMe</a> in Github for more information.<br>''')
    
    
    def showAbout(self):
        self.custSignal.message_printer.emit('''<br><b>STDF Fixer</b><br><br><b>Version: </b>{}<br><b>Author: </b>{}<br><b>Email: </b>{}<br><b>Repo: </b><a href="https://github.com/noonchen/stdfFixer">{}</a><br><br><span style="font-size:8pt">{}</span><br>'''.format("1.0.0", "Github@noonchen", "chennoon233@gmail.com", "noonchen/stdfFixer", "This application is licensed under GPL-3.0, special thanks to Casey Marshall for the open sourced module 'Pystdf'."))
    
    
    def startFix(self):
        input_path = self.line_std_input.toPlainText()
        dirout = self.line_std_output.toPlainText()
        output_path = os.path.join(dirout, ".".join(os.path.basename(input_path).split(".")[:-1])+"_Fixed@%s.std"%datetime.now().strftime("%Y%m%d_%H%M%S"))
        BinDef_path = self.line_BD_input.toPlainText()
        bdChecked = self.Use_BD.isChecked()
        
        inputValid = True
        if not os.path.isfile(input_path):
            self.custSignal.message_printer.emit('''<span style="color:red"><b>**{}**</b></span><br>'''.format("The path of the input std file is not valid"))
            inputValid = False
        elif dirout == "" or (not os.access(dirout, os.W_OK)):
            self.custSignal.message_printer.emit('''<span style="color:red"><b>**{}**</b></span><br>'''.format("The output path is empty or it has limited write permission"))
            inputValid = False
        elif not (os.path.isfile(BinDef_path) if bdChecked else True):
            self.custSignal.message_printer.emit('''<span style="color:red"><b>**{}**</b></span><br>'''.format("The path of the Bin Definition is not valid"))
            inputValid = False
        
        def callFix(input_path, output_path, BinDef_path, QSignal):
            stdfFixer(input_path=input_path, output_path=output_path, BinDefinition=BinDef_path, QSignal=QSignal)
        
        if inputValid:
            fix_t = threading.Thread(target=callFix, args=(input_path, output_path, BinDef_path, self.custSignal))
            fix_t.daemon = True
            fix_t.start() 


app = QApplication([])
app.setStyle('Fusion')
app_icon = QtGui.QIcon("Icon.png")
app.setWindowIcon(app_icon)
window = Fixer_UI()
window.show()
sys.exit(app.exec_())