# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'canvas.ui'
##
## Created by: Qt User Interface Compiler version 6.10.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (
    QCoreApplication,
    QDate,
    QDateTime,
    QLocale,
    QMetaObject,
    QObject,
    QPoint,
    QRect,
    QSize,
    QTime,
    QUrl,
    Qt,
)
from PySide6.QtGui import (
    QBrush,
    QColor,
    QConicalGradient,
    QCursor,
    QFont,
    QFontDatabase,
    QGradient,
    QIcon,
    QImage,
    QKeySequence,
    QLinearGradient,
    QPainter,
    QPalette,
    QPixmap,
    QRadialGradient,
    QTransform,
)
from PySide6.QtWidgets import (
    QApplication,
    QCheckBox,
    QFrame,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QSpinBox,
    QVBoxLayout,
    QWidget,
)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(918, 449)
        sizePolicy = QSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        sizePolicy.setHeightForWidth(
            self.centralwidget.sizePolicy().hasHeightForWidth()
        )
        self.centralwidget.setSizePolicy(sizePolicy)
        self.horizontalLayout = QHBoxLayout(self.centralwidget)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.plot_btn = QPushButton(self.centralwidget)
        self.plot_btn.setObjectName("plot_btn")

        self.verticalLayout.addWidget(self.plot_btn)

        self.center_btn = QPushButton(self.centralwidget)
        self.center_btn.setObjectName("center_btn")

        self.verticalLayout.addWidget(self.center_btn)

        self.clear_btn = QPushButton(self.centralwidget)
        self.clear_btn.setObjectName("clear_btn")

        self.verticalLayout.addWidget(self.clear_btn)

        self.grid_btn = QPushButton(self.centralwidget)
        self.grid_btn.setObjectName("grid_btn")

        self.verticalLayout.addWidget(self.grid_btn)

        self.cones_checkBox = QCheckBox(self.centralwidget)
        self.cones_checkBox.setObjectName("cones_checkBox")
        self.cones_checkBox.setEnabled(True)
        self.cones_checkBox.setChecked(True)

        self.verticalLayout.addWidget(self.cones_checkBox)

        self.func_lbl = QLabel(self.centralwidget)
        self.func_lbl.setObjectName("func_lbl")

        self.verticalLayout.addWidget(self.func_lbl)

        self.func_lineEdit = QLineEdit(self.centralwidget)
        self.func_lineEdit.setObjectName("func_lineEdit")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(
            self.func_lineEdit.sizePolicy().hasHeightForWidth()
        )
        self.func_lineEdit.setSizePolicy(sizePolicy1)

        self.verticalLayout.addWidget(self.func_lineEdit)

        self.from_lbl = QLabel(self.centralwidget)
        self.from_lbl.setObjectName("from_lbl")
        sizePolicy2 = QSizePolicy(
            QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum
        )
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.from_lbl.sizePolicy().hasHeightForWidth())
        self.from_lbl.setSizePolicy(sizePolicy2)

        self.verticalLayout.addWidget(self.from_lbl)

        self.from_spinBox = QSpinBox(self.centralwidget)
        self.from_spinBox.setObjectName("from_spinBox")
        self.from_spinBox.setMinimum(-999999999)
        self.from_spinBox.setMaximum(999999999)
        self.from_spinBox.setValue(-10)

        self.verticalLayout.addWidget(self.from_spinBox)

        self.to_lbl = QLabel(self.centralwidget)
        self.to_lbl.setObjectName("to_lbl")

        self.verticalLayout.addWidget(self.to_lbl)

        self.to_spinBox = QSpinBox(self.centralwidget)
        self.to_spinBox.setObjectName("to_spinBox")
        self.to_spinBox.setMinimum(-999999999)
        self.to_spinBox.setMaximum(999999999)
        self.to_spinBox.setValue(10)

        self.verticalLayout.addWidget(self.to_spinBox)

        self.dots_lbl = QLabel(self.centralwidget)
        self.dots_lbl.setObjectName("dots_lbl")

        self.verticalLayout.addWidget(self.dots_lbl)

        self.dots_spinBox = QSpinBox(self.centralwidget)
        self.dots_spinBox.setObjectName("dots_spinBox")
        self.dots_spinBox.setMinimum(10)
        self.dots_spinBox.setMaximum(1000)
        self.dots_spinBox.setValue(100)

        self.verticalLayout.addWidget(self.dots_spinBox)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.plot_wdgt = QFrame(self.centralwidget)
        self.plot_wdgt.setObjectName("plot_wdgt")
        sizePolicy.setHeightForWidth(self.plot_wdgt.sizePolicy().hasHeightForWidth())
        self.plot_wdgt.setSizePolicy(sizePolicy)
        self.plot_wdgt.setFrameShape(QFrame.Shape.Box)

        self.horizontalLayout.addWidget(self.plot_wdgt)

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)

    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", "MainWindow", None)
        )
        # if QT_CONFIG(whatsthis)
        self.plot_btn.setWhatsThis(
            QCoreApplication.translate(
                "MainWindow",
                "<html><head/><body><p>Press to plot chosen function</p></body></html>",
                None,
            )
        )
        # endif // QT_CONFIG(whatsthis)
        self.plot_btn.setText(QCoreApplication.translate("MainWindow", "Plot", None))
        self.center_btn.setText(
            QCoreApplication.translate("MainWindow", "Show center", None)
        )
        self.clear_btn.setText(QCoreApplication.translate("MainWindow", "Clear", None))
        self.grid_btn.setText(
            QCoreApplication.translate("MainWindow", "Build std grid", None)
        )
        self.cones_checkBox.setText(
            QCoreApplication.translate("MainWindow", "3D Cones", None)
        )
        self.func_lbl.setText(
            QCoreApplication.translate("MainWindow", "Function ", None)
        )
        self.func_lineEdit.setText(
            QCoreApplication.translate("MainWindow", "cos(x)", None)
        )
        self.from_lbl.setText(QCoreApplication.translate("MainWindow", "From", None))
        self.to_lbl.setText(QCoreApplication.translate("MainWindow", "To", None))
        self.dots_lbl.setText(
            QCoreApplication.translate("MainWindow", "Total dots", None)
        )

    # retranslateUi
