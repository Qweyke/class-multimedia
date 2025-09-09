# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'canvas.ui'
##
## Created by: Qt User Interface Compiler version 6.9.2
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
from PySide6.QtWidgets import (QApplication, QCheckBox, QDoubleSpinBox, QFrame,
    QHBoxLayout, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QSpinBox, QVBoxLayout,
    QWidget)

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
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        sizePolicy.setHeightForWidth(self.centralwidget.sizePolicy().hasHeightForWidth())
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.plot_btn = QPushButton(self.centralwidget)
        self.plot_btn.setObjectName(u"plot_btn")

        self.verticalLayout.addWidget(self.plot_btn)

        self.center_btn = QPushButton(self.centralwidget)
        self.center_btn.setObjectName(u"center_btn")

        self.verticalLayout.addWidget(self.center_btn)

        self.clear_btn = QPushButton(self.centralwidget)
        self.clear_btn.setObjectName(u"clear_btn")

        self.verticalLayout.addWidget(self.clear_btn)

        self.grid_btn = QPushButton(self.centralwidget)
        self.grid_btn.setObjectName(u"grid_btn")

        self.verticalLayout.addWidget(self.grid_btn)

        self.cones_checkBox = QCheckBox(self.centralwidget)
        self.cones_checkBox.setObjectName(u"cones_checkBox")
        self.cones_checkBox.setEnabled(True)
        self.cones_checkBox.setChecked(True)

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

        self.from_lbl = QLabel(self.centralwidget)
        self.from_lbl.setObjectName(u"from_lbl")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.from_lbl.sizePolicy().hasHeightForWidth())
        self.from_lbl.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.from_lbl)

        self.from_spinBox = QSpinBox(self.centralwidget)
        self.from_spinBox.setObjectName(u"from_spinBox")
        self.from_spinBox.setMinimum(-999999999)
        self.from_spinBox.setMaximum(999999999)
        self.from_spinBox.setValue(-10)

        self.verticalLayout.addWidget(self.from_spinBox)

        self.to_lbl = QLabel(self.centralwidget)
        self.to_lbl.setObjectName(u"to_lbl")

        self.verticalLayout.addWidget(self.to_lbl)

        self.to_spinBox = QSpinBox(self.centralwidget)
        self.to_spinBox.setObjectName(u"to_spinBox")
        self.to_spinBox.setMinimum(-999999999)
        self.to_spinBox.setMaximum(999999999)
        self.to_spinBox.setValue(10)

        self.verticalLayout.addWidget(self.to_spinBox)

        self.step_lbl = QLabel(self.centralwidget)
        self.step_lbl.setObjectName(u"step_lbl")

        self.verticalLayout.addWidget(self.step_lbl)

        self.step_spinBox = QDoubleSpinBox(self.centralwidget)
        self.step_spinBox.setObjectName(u"step_spinBox")
        self.step_spinBox.setMinimum(0.010000000000000)
        self.step_spinBox.setMaximum(9999999999999999635896294965248.000000000000000)
        self.step_spinBox.setSingleStep(0.010000000000000)
        self.step_spinBox.setValue(1.000000000000000)

        self.verticalLayout.addWidget(self.step_spinBox)


        self.horizontalLayout.addLayout(self.verticalLayout)

        self.plot_wdgt = QFrame(self.centralwidget)
        self.plot_wdgt.setObjectName(u"plot_wdgt")
        sizePolicy.setHeightForWidth(self.plot_wdgt.sizePolicy().hasHeightForWidth())
        self.plot_wdgt.setSizePolicy(sizePolicy)
        self.plot_wdgt.setFrameShape(QFrame.Box)

        self.horizontalLayout.addWidget(self.plot_wdgt)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
#if QT_CONFIG(whatsthis)
        self.plot_btn.setWhatsThis(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Press to plot chosen function</p></body></html>", None))
#endif // QT_CONFIG(whatsthis)
        self.plot_btn.setText(QCoreApplication.translate("MainWindow", u"Plot", None))
        self.center_btn.setText(QCoreApplication.translate("MainWindow", u"Show center", None))
        self.clear_btn.setText(QCoreApplication.translate("MainWindow", u"Clear", None))
        self.grid_btn.setText(QCoreApplication.translate("MainWindow", u"Build std grid", None))
        self.cones_checkBox.setText(QCoreApplication.translate("MainWindow", u"Cones", None))
        self.func_lbl.setText(QCoreApplication.translate("MainWindow", u"Function ", None))
        self.func_lineEdit.setText(QCoreApplication.translate("MainWindow", u"cos(x)", None))
        self.from_lbl.setText(QCoreApplication.translate("MainWindow", u"From", None))
        self.to_lbl.setText(QCoreApplication.translate("MainWindow", u"To", None))
        self.step_lbl.setText(QCoreApplication.translate("MainWindow", u"Step", None))
    # retranslateUi

