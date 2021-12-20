from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Exalemao(object):
    def setupUi(self, AL):
        AL.setObjectName("AL")
        AL.resize(310, 161)
        AL.setMinimumSize(QtCore.QSize(310, 161))
        AL.setMaximumSize(QtCore.QSize(310, 161))
        font = QtGui.QFont()
        font.setFamily("Segoe UI")
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        AL.setFont(font)
        AL.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(AL)
        self.centralwidget.setObjectName("centralwidget")
        self.start = QtWidgets.QPushButton(self.centralwidget)
        self.start.setGeometry(QtCore.QRect(20, 40, 271, 51))
        self.start.setAutoFillBackground(False)
        self.start.setStyleSheet(
            'font: 75 9pt "Segoe UI";\n'
            "font-weight: bold;\n"
            "background-color: rgb(231, 179, 1);\n"
            "border-style: outset;\n"
            "border-radius: 5px;"
        )
        self.start.setObjectName("start")
        self.move_furni = QtWidgets.QCheckBox(self.centralwidget)
        self.move_furni.setGeometry(QtCore.QRect(20, 110, 810, 17))
        self.move_furni.setObjectName("move_furni")
        self.move_wall = QtWidgets.QCheckBox(self.centralwidget)
        self.move_wall.setGeometry(QtCore.QRect(20, 130, 810, 17))
        self.move_wall.setObjectName("move_wall")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(50, 10, 300, 16))
        self.label.setObjectName("label")
        self.room_loaded = QtWidgets.QLabel(self.centralwidget)
        self.room_loaded.setGeometry(QtCore.QRect(160, 130, 300, 16))
        self.room_loaded.setStyleSheet(
            "color: rgb(155, 0, 0);\n" "font-weight: bold;"
        )
        self.room_loaded.setObjectName("room_loaded")
        self.room_loaded.setHidden(True)
        AL.setCentralWidget(self.centralwidget)

        self.retranslateUi(AL)
        QtCore.QMetaObject.connectSlotsByName(AL)

    def retranslateUi(self, AL):
        _translate = QtCore.QCoreApplication.translate
        AL.setWindowTitle(_translate("AL", "Meine Ehre heißt Treue"))
        self.start.setText(_translate("AL", "Iniciar"))
        self.move_furni.setText(_translate("AL", "Mover Mobis"))
        self.move_wall.setText(_translate("AL", "Mover Paredes"))
        self.label.setText(_translate("AL", "Minha honra chama-se lealdade!"))
        self.room_loaded.setText(_translate("AL", "Quarto Carregado"))
