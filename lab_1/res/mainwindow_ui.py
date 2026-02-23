# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'mainwindow.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractSpinBox, QApplication, QCheckBox, QDoubleSpinBox,
    QFrame, QHBoxLayout, QLabel, QLineEdit,
    QMainWindow, QPushButton, QSizePolicy, QSpinBox,
    QVBoxLayout, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(918, 449)
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.ListAdd))
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.clear_btn = QPushButton(self.centralwidget)
        self.clear_btn.setObjectName(u"clear_btn")

        self.verticalLayout.addWidget(self.clear_btn)

        self.cones_checkBox = QCheckBox(self.centralwidget)
        self.cones_checkBox.setObjectName(u"cones_checkBox")
        self.cones_checkBox.setEnabled(True)
        self.cones_checkBox.setChecked(False)

        self.verticalLayout.addWidget(self.cones_checkBox)

        self.func_lbl = QLabel(self.centralwidget)
        self.func_lbl.setObjectName(u"func_lbl")

        self.verticalLayout.addWidget(self.func_lbl)

        self.func_lineEdit = QLineEdit(self.centralwidget)
        self.func_lineEdit.setObjectName(u"func_lineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.func_lineEdit.sizePolicy().hasHeightForWidth())
        self.func_lineEdit.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.func_lineEdit)

        self.funcs_frame = QFrame(self.centralwidget)
        self.funcs_frame.setObjectName(u"funcs_frame")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.funcs_frame.sizePolicy().hasHeightForWidth())
        self.funcs_frame.setSizePolicy(sizePolicy2)
        self.funcs_frame.setMaximumSize(QSize(200, 200))
        self.funcs_frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.funcs_frame.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout.addWidget(self.funcs_frame)

        self.add_btn = QPushButton(self.centralwidget)
        self.add_btn.setObjectName(u"add_btn")

        self.verticalLayout.addWidget(self.add_btn)

        self.from_lbl = QLabel(self.centralwidget)
        self.from_lbl.setObjectName(u"from_lbl")
        sizePolicy2.setHeightForWidth(self.from_lbl.sizePolicy().hasHeightForWidth())
        self.from_lbl.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.from_lbl)

        self.from_doubleSpinBox = QDoubleSpinBox(self.centralwidget)
        self.from_doubleSpinBox.setObjectName(u"from_doubleSpinBox")
        self.from_doubleSpinBox.setDecimals(3)
        self.from_doubleSpinBox.setMinimum(-10000.000000000000000)
        self.from_doubleSpinBox.setMaximum(1000.000000000000000)
        self.from_doubleSpinBox.setSingleStep(0.001000000000000)
        self.from_doubleSpinBox.setStepType(QAbstractSpinBox.StepType.AdaptiveDecimalStepType)
        self.from_doubleSpinBox.setValue(-10.000000000000000)

        self.verticalLayout.addWidget(self.from_doubleSpinBox)

        self.to_lbl = QLabel(self.centralwidget)
        self.to_lbl.setObjectName(u"to_lbl")

        self.verticalLayout.addWidget(self.to_lbl)

        self.to_doubleSpinBox = QDoubleSpinBox(self.centralwidget)
        self.to_doubleSpinBox.setObjectName(u"to_doubleSpinBox")
        self.to_doubleSpinBox.setDecimals(3)
        self.to_doubleSpinBox.setMinimum(-1000.000000000000000)
        self.to_doubleSpinBox.setMaximum(1000.000000000000000)
        self.to_doubleSpinBox.setSingleStep(0.001000000000000)
        self.to_doubleSpinBox.setStepType(QAbstractSpinBox.StepType.AdaptiveDecimalStepType)
        self.to_doubleSpinBox.setValue(10.000000000000000)

        self.verticalLayout.addWidget(self.to_doubleSpinBox)

        self.func_points_lbl = QLabel(self.centralwidget)
        self.func_points_lbl.setObjectName(u"func_points_lbl")

        self.verticalLayout.addWidget(self.func_points_lbl)

        self.func_points_spinBox = QSpinBox(self.centralwidget)
        self.func_points_spinBox.setObjectName(u"func_points_spinBox")
        self.func_points_spinBox.setMinimum(5)
        self.func_points_spinBox.setMaximum(10000)
        self.func_points_spinBox.setValue(100)

        self.verticalLayout.addWidget(self.func_points_spinBox)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.plot_wdgt = QFrame(self.centralwidget)
        self.plot_wdgt.setObjectName(u"plot_wdgt")
        sizePolicy.setHeightForWidth(self.plot_wdgt.sizePolicy().hasHeightForWidth())
        self.plot_wdgt.setSizePolicy(sizePolicy)
        self.plot_wdgt.setFrameShape(QFrame.Shape.Box)

        self.horizontalLayout.addWidget(self.plot_wdgt)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"QweykePlotter", None))
        self.clear_btn.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.cones_checkBox.setText(QCoreApplication.translate("MainWindow", u"3D Cones", None))
        self.func_lbl.setText(QCoreApplication.translate("MainWindow", u"Current function(s)", None))
        self.func_lineEdit.setText(QCoreApplication.translate("MainWindow", u"cos(x)", None))
        self.add_btn.setText(QCoreApplication.translate("MainWindow", u"Add function", None))
        self.from_lbl.setText(QCoreApplication.translate("MainWindow", u"From", None))
        self.to_lbl.setText(QCoreApplication.translate("MainWindow", u"To", None))
        self.func_points_lbl.setText(QCoreApplication.translate("MainWindow", u"Function points", None))
    # retranslateUi

