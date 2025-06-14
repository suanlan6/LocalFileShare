# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'main.ui'
##
## Created by: Qt User Interface Compiler version 6.9.1
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
from PySide6.QtWidgets import (QAbstractItemView, QApplication, QFrame, QGridLayout,
    QHBoxLayout, QHeaderView, QLabel, QMainWindow,
    QPushButton, QSizePolicy, QStackedWidget, QTableWidget,
    QTableWidgetItem, QVBoxLayout, QWidget)

from draggable_table import DraggableTableWidget
from hover_table import HoverableTable
import resources_rc

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1280, 712)
        MainWindow.setMinimumSize(QSize(940, 560))
        self.styleSheet = QWidget(MainWindow)
        self.styleSheet.setObjectName(u"styleSheet")
        font = QFont()
        font.setFamilies([u"Segoe UI"])
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        self.styleSheet.setFont(font)
        self.styleSheet.setStyleSheet(u"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"\n"
"SET APP STYLESHEET - FULL STYLES HERE\n"
"DARK THEME - DRACULA COLOR BASED\n"
"\n"
"# BY: WANDERSON M.PIMENTA\n"
"# PROJECT MADE WITH: Qt Designer and PySide6\n"
"# V: 1.0.0\n"
"#\n"
"# This project can be used freely for all uses, as long as they maintain the\n"
"# respective credits only in the Python scripts, any information in the visual\n"
"# interface (GUI) can be modified without any implication.\n"
"#\n"
"# There are limitations on Qt licenses if you want to use your products\n"
"# commercially, I recommend reading them on the official website:\n"
"# https://doc.qt.io/qtforpython/licenses.html\n"
"\n"
"///////////////////////////////////////////////////////////////////////////////////////////////// */\n"
"\n"
"QWidget{\n"
"	color: #333;\n"
"	font: 10pt \"Segoe UI\";\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Tooltip */"
                        "\n"
"QToolTip {\n"
"	color: #333;\n"
"	background-color: #f8f8f2;\n"
"	border: 1px solid #CCC;\n"
"	background-image: none;\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 2px solid rgb(255, 121, 198);\n"
"	text-align: left;\n"
"	padding-left: 8px;\n"
"	margin: 0px;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Bg App */\n"
"#bgApp {	\n"
"	background-color: #f8f8f2;\n"
"	border: 1px solid #CCC;\n"
"    color: #44475a;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Left Menu */\n"
"#leftMenuBg {	\n"
"	background-color: #6272a4;\n"
"}\n"
"#topLogo {\n"
"	background-color: #6272a4;\n"
"	background-image: url(:/images/images/MNS.png);\n"
"	background-position: centered;\n"
"	background-repeat: no-repeat;\n"
"}\n"
"#titleLeftApp { font: 63 12pt \"Segoe UI Semibold\"; color: #f8f8f2; }\n"
"#titleLeftDescrip"
                        "tion { font: 8pt \"Segoe UI\"; color: #bd93f9; }\n"
"\n"
"/* MENUS */\n"
"#topMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color: transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"    color: #f8f8f2;\n"
"}\n"
"#topMenu .QPushButton:hover {\n"
"	background-color: #bd93f9;\n"
"}\n"
"#topMenu .QPushButton:pressed {	\n"
"	background-color: #ff79c6;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#bottomMenu .QPushButton {	\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"    color: #f8f8f2;\n"
"}\n"
"#bottomMenu .QPushButton:hover {\n"
"	background-color: #bd93f9;\n"
"}\n"
"#bottomMenu .QPushButton:pressed {	\n"
"	background-color: #ff79c6;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"#leftMenuFrame{\n"
"	bo"
                        "rder-top: 3px solid #6a7cb1;\n"
"}\n"
"\n"
"/* Toggle Button */\n"
"#toggleButton {\n"
"	background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 20px solid transparent;\n"
"	background-color: #5b6996;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"	color: #f8f8f2;\n"
"}\n"
"#toggleButton:hover {\n"
"	background-color: #bd93f9;\n"
"}\n"
"#toggleButton:pressed {	\n"
"	background-color: #ff79c6;\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"\n"
"/* Title Menu */\n"
"#titleRightInfo { padding-left: 10px; }\n"
"\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Extra Tab */\n"
"#extraLeftBox {	\n"
"	background-color: #495474;\n"
"    color: #f8f8f2;\n"
"}\n"
"#extraTopBg{	\n"
"	background-color: rgb(189, 147, 249)\n"
"}\n"
"\n"
"/* Icon */\n"
"#extraIcon {\n"
"	background-position: center;\n"
"	background-repeat: no-repeat;\n"
"	background-image: url(:/icons/icons/icon_settings.png);\n"
"}\n"
"\n"
""
                        "/* Label */\n"
"#extraLabel { color: rgb(255, 255, 255); }\n"
"\n"
"/* Btn Close */\n"
"#extraCloseColumnBtn { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#extraCloseColumnBtn:hover { background-color: rgb(196, 161, 249); border-style: solid; border-radius: 4px; }\n"
"#extraCloseColumnBtn:pressed { background-color: rgb(180, 141, 238); border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Extra Content */\n"
"#extraContent{\n"
"	border-top: 3px solid #6272a4;\n"
"}\n"
"\n"
"/* Extra Top Menus */\n"
"#extraTopMenu .QPushButton {\n"
"    background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"    color: #f8f8f2;\n"
"}\n"
"#extraTopMenu .QPushButton:hover {\n"
"	background-color: #5d6c99;\n"
"}\n"
"#extraTopMenu .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
""
                        "}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Content App */\n"
"#contentTopBg{	\n"
"	background-color: #6272a4;\n"
"}\n"
"#contentBottom{\n"
"	border-top: 3px solid #bd93f9;\n"
"}\n"
"#titleRightInfo{\n"
"    color: #f8f8f2;\n"
"}\n"
"\n"
"/* Top Buttons */\n"
"#rightButtons .QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"#rightButtons .QPushButton:hover { background-color: #bd93f9; border-style: solid; border-radius: 4px; }\n"
"#rightButtons .QPushButton:pressed { background-color: #ff79c6; border-style: solid; border-radius: 4px; }\n"
"\n"
"/* Theme Settings */\n"
"#extraRightBox { background-color: #495474; }\n"
"#themeSettingsTopDetail { background-color: #6272a4; }\n"
"\n"
"/* Bottom Bar */\n"
"#bottomBar { background-color: #495474 }\n"
"#bottomBar QLabel { font-size: 11px; color: #f8f8f2; padding-left: 10px; padding-right: 10px; padding-bottom: 2px; }\n"
"\n"
"/* CONTENT SETTINGS */\n"
""
                        "/* MENUS */\n"
"#contentSettings .QPushButton {\n"
"    background-position: left center;\n"
"    background-repeat: no-repeat;\n"
"	border: none;\n"
"	border-left: 22px solid transparent;\n"
"	background-color:transparent;\n"
"	text-align: left;\n"
"	padding-left: 44px;\n"
"    color: #f8f8f2;\n"
"}\n"
"#contentSettings .QPushButton:hover {\n"
"	background-color: #5d6c99;\n"
"}\n"
"#contentSettings .QPushButton:pressed {	\n"
"	background-color: rgb(189, 147, 249);\n"
"	color: rgb(255, 255, 255);\n"
"}\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"QTableWidget */\n"
"QTableWidget {	\n"
"	background-color: transparent;\n"
"	padding: 10px;\n"
"	border-radius: 5px;\n"
"	gridline-color: #9faeda;\n"
"    outline: none;\n"
"}\n"
"QTableWidget::item{\n"
"	border-color: #9faeda;\n"
"	padding-left: 5px;\n"
"	padding-right: 5px;\n"
"	gridline-color: #9faeda;\n"
"}\n"
"QTableWidget::item:selected{\n"
"	background-color: rgb(189, 147, 249);\n"
"    color: #f8f"
                        "8f2;\n"
"}\n"
"QHeaderView::section{\n"
"	background-color: #6272a4;\n"
"	max-width: 30px;\n"
"	border: none;\n"
"	border-style: none;\n"
"}\n"
"QTableWidget::horizontalHeader {	\n"
"	background-color: #6272a4;\n"
"}\n"
"QHeaderView::section:horizontal\n"
"{\n"
"    border: 1px solid #6272a4;\n"
"	background-color: #6272a4;\n"
"	padding: 3px;\n"
"	border-top-left-radius: 7px;\n"
"    border-top-right-radius: 7px;\n"
"    color: #f8f8f2;\n"
"}\n"
"QHeaderView::section:vertical\n"
"{\n"
"    border: 1px solid #6272a4;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"LineEdit */\n"
"QLineEdit {\n"
"	background-color: #6272a4;\n"
"	border-radius: 5px;\n"
"	border: 2px solid #6272a4;\n"
"	padding-left: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"    color: #f8f8f2;\n"
"}\n"
"QLineEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QLineEdit:focus {\n"
"	border: 2px solid #ff"
                        "79c6;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"PlainTextEdit */\n"
"QPlainTextEdit {\n"
"	background-color: #6272a4;\n"
"	border-radius: 5px;\n"
"	padding: 10px;\n"
"	selection-color: rgb(255, 255, 255);\n"
"	selection-background-color: rgb(255, 121, 198);\n"
"    color: #f8f8f2;\n"
"}\n"
"QPlainTextEdit  QScrollBar:vertical {\n"
"    width: 8px;\n"
" }\n"
"QPlainTextEdit  QScrollBar:horizontal {\n"
"    height: 8px;\n"
" }\n"
"QPlainTextEdit:hover {\n"
"	border: 2px solid rgb(64, 71, 88);\n"
"}\n"
"QPlainTextEdit:focus {\n"
"	border: 2px solid #ff79c6;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ScrollBars */\n"
"QScrollBar:horizontal {\n"
"    border: none;\n"
"    background: #6272a4;\n"
"    height: 8px;\n"
"    margin: 0px 21px 0 21px;\n"
"	border-radius: 0px;\n"
"}\n"
"QScrollBar::handle:horizontal {\n"
"    background: rgb(189, 147, 249);\n"
"    min-"
                        "width: 25px;\n"
"	border-radius: 4px\n"
"}\n"
"QScrollBar::add-line:horizontal {\n"
"    border: none;\n"
"    background: #6272a4;\n"
"    width: 20px;\n"
"	border-top-right-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    subcontrol-position: right;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::sub-line:horizontal {\n"
"    border: none;\n"
"    background: #6272a4;\n"
"    width: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-bottom-left-radius: 4px;\n"
"    subcontrol-position: left;\n"
"    subcontrol-origin: margin;\n"
"}\n"
"QScrollBar::up-arrow:horizontal, QScrollBar::down-arrow:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
"QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal\n"
"{\n"
"     background: none;\n"
"}\n"
" QScrollBar:vertical {\n"
"	border: none;\n"
"    background-color: #6272a4;\n"
"    width: 8px;\n"
"    margin: 21px 0 21px 0;\n"
"	border-radius: 0px;\n"
" }\n"
" QScrollBar::handle:vertical {	\n"
"	background: rgb(189, 147, 249);\n"
""
                        "    min-height: 25px;\n"
"	border-radius: 4px\n"
" }\n"
" QScrollBar::add-line:vertical {\n"
"     border: none;\n"
"    background: #6272a4;\n"
"     height: 20px;\n"
"	border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"     subcontrol-position: bottom;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::sub-line:vertical {\n"
"	border: none;\n"
"    background: #6272a4;\n"
"     height: 20px;\n"
"	border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"     subcontrol-position: top;\n"
"     subcontrol-origin: margin;\n"
" }\n"
" QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
" QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {\n"
"     background: none;\n"
" }\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CheckBox */\n"
"QCheckBox::indicator {\n"
"    border: 3px solid #6272a4;\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	bo"
                        "rder-radius: 10px;\n"
"    background: #6272a4;\n"
"}\n"
"QCheckBox::indicator:hover {\n"
"    border: 3px solid rgb(119, 136, 187);\n"
"}\n"
"QCheckBox::indicator:checked {\n"
"    background: 3px solid #bd93f9;\n"
"	border: 3px solid #bd93f9;	\n"
"	background-image: url(:/icons/icons/cil-check-alt.png);\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"RadioButton */\n"
"QRadioButton::indicator {\n"
"    border: 3px solid #6272a4;\n"
"	width: 15px;\n"
"	height: 15px;\n"
"	border-radius: 10px;\n"
"    background: #6272a4;\n"
"}\n"
"QRadioButton::indicator:hover {\n"
"    border: 3px solid rgb(119, 136, 187);\n"
"}\n"
"QRadioButton::indicator:checked {\n"
"    background: 3px solid #bd93f9;\n"
"	border: 3px solid #bd93f9;	\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"ComboBox */\n"
"QComboBox{\n"
"	background-color: #6272a4;\n"
"	border-radius: 5px;\n"
"	border: 2px s"
                        "olid #6272a4;\n"
"	padding: 5px;\n"
"	padding-left: 10px;\n"
"    color: #f8f8f2;\n"
"}\n"
"QComboBox:hover{\n"
"	border: 2px solid #7284b9;\n"
"}\n"
"QComboBox::drop-down {\n"
"	subcontrol-origin: padding;\n"
"	subcontrol-position: top right;\n"
"	width: 25px; \n"
"	border-left-width: 3px;\n"
"	border-left-color: #6272a4;\n"
"	border-left-style: solid;\n"
"	border-top-right-radius: 3px;\n"
"	border-bottom-right-radius: 3px;	\n"
"	background-image: url(:/icons/icons/cil-arrow-bottom.png);\n"
"	background-position: center;\n"
"	background-repeat: no-reperat;\n"
" }\n"
"QComboBox QAbstractItemView {\n"
"	color: rgb(255, 121, 198);	\n"
"	background-color: #6272a4;\n"
"	padding: 10px;\n"
"	selection-background-color: #6272a4;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Sliders */\n"
"QSlider::groove:horizontal {\n"
"    border-radius: 5px;\n"
"    height: 10px;\n"
"	margin: 0px;\n"
"	background-color: #6272a4;\n"
"}\n"
"QSlider::groove:hor"
                        "izontal:hover {\n"
"	background-color: #6272a4;\n"
"}\n"
"QSlider::handle:horizontal {\n"
"    background-color: rgb(189, 147, 249);\n"
"    border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:horizontal:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:horizontal:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
"\n"
"QSlider::groove:vertical {\n"
"    border-radius: 5px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	background-color: #6272a4;\n"
"}\n"
"QSlider::groove:vertical:hover {\n"
"	background-color: #6272a4;\n"
"}\n"
"QSlider::handle:vertical {\n"
"    background-color: rgb(189, 147, 249);\n"
"	border: none;\n"
"    height: 10px;\n"
"    width: 10px;\n"
"    margin: 0px;\n"
"	border-radius: 5px;\n"
"}\n"
"QSlider::handle:vertical:hover {\n"
"    background-color: rgb(195, 155, 255);\n"
"}\n"
"QSlider::handle:vertical:pressed {\n"
"    background-color: rgb(255, 121, 198);\n"
"}\n"
""
                        "\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"CommandLinkButton */\n"
"#pagesContainer QCommandLinkButton {	\n"
"	color: rgb(255, 121, 198);\n"
"	border-radius: 5px;\n"
"	padding: 5px;\n"
"    border: 2px solid #ff79c6;\n"
"    color: #ff79c6;\n"
"}\n"
"#pagesContainer QCommandLinkButton:hover {	\n"
"	color: rgb(255, 170, 255);\n"
"	background-color: #6272a4;\n"
"}\n"
"#pagesContainer QCommandLinkButton:pressed {	\n"
"	color: rgb(189, 147, 249);\n"
"	background-color: #586796;\n"
"}\n"
"\n"
"/* /////////////////////////////////////////////////////////////////////////////////////////////////\n"
"Button */\n"
"#pagesContainer QPushButton {\n"
"	border: 2px solid #6272a4;\n"
"	border-radius: 5px;	\n"
"	background-color: #6272a4;\n"
"    color: #f8f8f2;\n"
"}\n"
"#pagesContainer QPushButton:hover {\n"
"	background-color: #7082b6;\n"
"	border: 2px solid #7082b6;\n"
"}\n"
"#pagesContainer QPushButton:pressed {	\n"
"	background-color: #546391;\n"
"	borde"
                        "r: 2px solid #ff79c6;\n"
"}\n"
"\n"
"\n"
"")
        self.horizontalLayout_7 = QHBoxLayout(self.styleSheet)
        self.horizontalLayout_7.setObjectName(u"horizontalLayout_7")
        self.bgApp = QFrame(self.styleSheet)
        self.bgApp.setObjectName(u"bgApp")
        self.bgApp.setStyleSheet(u"")
        self.bgApp.setFrameShape(QFrame.Shape.NoFrame)
        self.bgApp.setFrameShadow(QFrame.Shadow.Raised)
        self.appLayout = QHBoxLayout(self.bgApp)
        self.appLayout.setSpacing(0)
        self.appLayout.setObjectName(u"appLayout")
        self.appLayout.setContentsMargins(0, 0, 0, 0)
        self.leftMenuBg = QFrame(self.bgApp)
        self.leftMenuBg.setObjectName(u"leftMenuBg")
        self.leftMenuBg.setMinimumSize(QSize(60, 0))
        self.leftMenuBg.setMaximumSize(QSize(60, 16777215))
        self.leftMenuBg.setFrameShape(QFrame.Shape.NoFrame)
        self.leftMenuBg.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_3 = QVBoxLayout(self.leftMenuBg)
        self.verticalLayout_3.setSpacing(0)
        self.verticalLayout_3.setObjectName(u"verticalLayout_3")
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.topLogoInfo = QFrame(self.leftMenuBg)
        self.topLogoInfo.setObjectName(u"topLogoInfo")
        self.topLogoInfo.setMinimumSize(QSize(0, 50))
        self.topLogoInfo.setMaximumSize(QSize(16777215, 50))
        self.topLogoInfo.setFrameShape(QFrame.Shape.NoFrame)
        self.topLogoInfo.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_3.addWidget(self.topLogoInfo)

        self.leftMenuFrame = QFrame(self.leftMenuBg)
        self.leftMenuFrame.setObjectName(u"leftMenuFrame")
        self.leftMenuFrame.setFrameShape(QFrame.Shape.NoFrame)
        self.leftMenuFrame.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalMenuLayout = QVBoxLayout(self.leftMenuFrame)
        self.verticalMenuLayout.setSpacing(0)
        self.verticalMenuLayout.setObjectName(u"verticalMenuLayout")
        self.verticalMenuLayout.setContentsMargins(0, 0, 0, 0)
        self.toggleBox = QFrame(self.leftMenuFrame)
        self.toggleBox.setObjectName(u"toggleBox")
        self.toggleBox.setMaximumSize(QSize(16777215, 45))
        self.toggleBox.setFrameShape(QFrame.Shape.NoFrame)
        self.toggleBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_4 = QVBoxLayout(self.toggleBox)
        self.verticalLayout_4.setSpacing(0)
        self.verticalLayout_4.setObjectName(u"verticalLayout_4")
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.toggleButton = QPushButton(self.toggleBox)
        self.toggleButton.setObjectName(u"toggleButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.toggleButton.sizePolicy().hasHeightForWidth())
        self.toggleButton.setSizePolicy(sizePolicy)
        self.toggleButton.setMinimumSize(QSize(0, 45))
        self.toggleButton.setFont(font)
        self.toggleButton.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.toggleButton.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.toggleButton.setStyleSheet(u"background-image: url(:/icons/icons/icon_menu.png);")

        self.verticalLayout_4.addWidget(self.toggleButton)


        self.verticalMenuLayout.addWidget(self.toggleBox)

        self.topMenu = QFrame(self.leftMenuFrame)
        self.topMenu.setObjectName(u"topMenu")
        self.topMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.topMenu.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_8 = QVBoxLayout(self.topMenu)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.btn_home = QPushButton(self.topMenu)
        self.btn_home.setObjectName(u"btn_home")
        sizePolicy.setHeightForWidth(self.btn_home.sizePolicy().hasHeightForWidth())
        self.btn_home.setSizePolicy(sizePolicy)
        self.btn_home.setMinimumSize(QSize(0, 45))
        self.btn_home.setFont(font)
        self.btn_home.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_home.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_home.setStyleSheet(u"background-image: url(:/icons/icons/cil-home.png);")

        self.verticalLayout_8.addWidget(self.btn_home)

        self.btn_widgets = QPushButton(self.topMenu)
        self.btn_widgets.setObjectName(u"btn_widgets")
        sizePolicy.setHeightForWidth(self.btn_widgets.sizePolicy().hasHeightForWidth())
        self.btn_widgets.setSizePolicy(sizePolicy)
        self.btn_widgets.setMinimumSize(QSize(0, 45))
        self.btn_widgets.setFont(font)
        self.btn_widgets.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_widgets.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_widgets.setStyleSheet(u"background-image: url(:/icons/icons/cil-file.png);")

        self.verticalLayout_8.addWidget(self.btn_widgets)

        self.btn_new = QPushButton(self.topMenu)
        self.btn_new.setObjectName(u"btn_new")
        sizePolicy.setHeightForWidth(self.btn_new.sizePolicy().hasHeightForWidth())
        self.btn_new.setSizePolicy(sizePolicy)
        self.btn_new.setMinimumSize(QSize(0, 45))
        self.btn_new.setFont(font)
        self.btn_new.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_new.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_new.setStyleSheet(u"background-image: url(:/icons/icons/cil-chat-bubble.png);")

        self.verticalLayout_8.addWidget(self.btn_new)


        self.verticalMenuLayout.addWidget(self.topMenu, 0, Qt.AlignmentFlag.AlignTop)

        self.bottomMenu = QFrame(self.leftMenuFrame)
        self.bottomMenu.setObjectName(u"bottomMenu")
        self.bottomMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.bottomMenu.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_9 = QVBoxLayout(self.bottomMenu)
        self.verticalLayout_9.setSpacing(0)
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.verticalLayout_9.setContentsMargins(0, 0, 0, 0)

        self.verticalMenuLayout.addWidget(self.bottomMenu, 0, Qt.AlignmentFlag.AlignBottom)


        self.verticalLayout_3.addWidget(self.leftMenuFrame)


        self.appLayout.addWidget(self.leftMenuBg)

        self.extraLeftBox = QFrame(self.bgApp)
        self.extraLeftBox.setObjectName(u"extraLeftBox")
        self.extraLeftBox.setMinimumSize(QSize(0, 0))
        self.extraLeftBox.setMaximumSize(QSize(0, 16777215))
        self.extraLeftBox.setFrameShape(QFrame.Shape.NoFrame)
        self.extraLeftBox.setFrameShadow(QFrame.Shadow.Raised)
        self.extraColumLayout = QVBoxLayout(self.extraLeftBox)
        self.extraColumLayout.setSpacing(0)
        self.extraColumLayout.setObjectName(u"extraColumLayout")
        self.extraColumLayout.setContentsMargins(0, 0, 0, 0)
        self.extraTopBg = QFrame(self.extraLeftBox)
        self.extraTopBg.setObjectName(u"extraTopBg")
        self.extraTopBg.setMinimumSize(QSize(0, 50))
        self.extraTopBg.setMaximumSize(QSize(16777215, 50))
        self.extraTopBg.setFrameShape(QFrame.Shape.NoFrame)
        self.extraTopBg.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_5 = QVBoxLayout(self.extraTopBg)
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setObjectName(u"verticalLayout_5")
        self.verticalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.extraTopLayout = QGridLayout()
        self.extraTopLayout.setObjectName(u"extraTopLayout")
        self.extraTopLayout.setHorizontalSpacing(10)
        self.extraTopLayout.setVerticalSpacing(0)
        self.extraTopLayout.setContentsMargins(10, -1, 10, -1)
        self.extraLabel = QLabel(self.extraTopBg)
        self.extraLabel.setObjectName(u"extraLabel")
        self.extraLabel.setMinimumSize(QSize(150, 0))
        self.extraLabel.setStyleSheet(u"QLabel {\n"
"    color: white;\n"
"    font-size: 12pt;\n"
"    font-weight: bold;\n"
"    padding: 0.3em 0.6em;\n"
"}")

        self.extraTopLayout.addWidget(self.extraLabel, 0, 1, 1, 1)

        self.pushButton_4 = QPushButton(self.extraTopBg)
        self.pushButton_4.setObjectName(u"pushButton_4")
        self.pushButton_4.setMinimumSize(QSize(28, 28))
        self.pushButton_4.setMaximumSize(QSize(28, 28))
        self.pushButton_4.setStyleSheet(u"QPushButton { background-color: rgba(255, 255, 255, 0); border: none;  border-radius: 5px; }\n"
"")
        icon = QIcon()
        icon.addFile(u":/icons/icons/cil-devices.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton_4.setIcon(icon)

        self.extraTopLayout.addWidget(self.pushButton_4, 0, 0, 1, 1)

        self.extraCloseColumnBtn = QPushButton(self.extraTopBg)
        self.extraCloseColumnBtn.setObjectName(u"extraCloseColumnBtn")
        self.extraCloseColumnBtn.setMinimumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setMaximumSize(QSize(28, 28))
        self.extraCloseColumnBtn.setCursor(QCursor(Qt.CursorShape.ArrowCursor))
        self.extraCloseColumnBtn.setMouseTracking(True)
        icon1 = QIcon()
        icon1.addFile(u":/icons/icons/icon_close.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.extraCloseColumnBtn.setIcon(icon1)
        self.extraCloseColumnBtn.setIconSize(QSize(20, 20))

        self.extraTopLayout.addWidget(self.extraCloseColumnBtn, 0, 2, 1, 1)


        self.verticalLayout_5.addLayout(self.extraTopLayout)


        self.extraColumLayout.addWidget(self.extraTopBg)

        self.extraContent = QFrame(self.extraLeftBox)
        self.extraContent.setObjectName(u"extraContent")
        self.extraContent.setFrameShape(QFrame.Shape.NoFrame)
        self.extraContent.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_12 = QVBoxLayout(self.extraContent)
        self.verticalLayout_12.setSpacing(0)
        self.verticalLayout_12.setObjectName(u"verticalLayout_12")
        self.verticalLayout_12.setContentsMargins(0, 0, 0, 0)
        self.extraTopMenu = QFrame(self.extraContent)
        self.extraTopMenu.setObjectName(u"extraTopMenu")
        self.extraTopMenu.setFrameShape(QFrame.Shape.NoFrame)
        self.extraTopMenu.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_11 = QVBoxLayout(self.extraTopMenu)
        self.verticalLayout_11.setSpacing(0)
        self.verticalLayout_11.setObjectName(u"verticalLayout_11")
        self.verticalLayout_11.setContentsMargins(0, 0, 0, 0)
        self.btn_adjustments = QPushButton(self.extraTopMenu)
        self.btn_adjustments.setObjectName(u"btn_adjustments")
        sizePolicy.setHeightForWidth(self.btn_adjustments.sizePolicy().hasHeightForWidth())
        self.btn_adjustments.setSizePolicy(sizePolicy)
        self.btn_adjustments.setMinimumSize(QSize(0, 45))
        self.btn_adjustments.setFont(font)
        self.btn_adjustments.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_adjustments.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_adjustments.setStyleSheet(u"QPushButton {\n"
"	background-image: url(:/icons/icons/cil-find-in-page.png);\n"
"}\n"
"QPushButton :hover {\n"
"    background-color: palette(light);\n"
"    border-radius: 0.2em;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: palette(mid);\n"
"}\n"
"")

        self.verticalLayout_11.addWidget(self.btn_adjustments)


        self.verticalLayout_12.addWidget(self.extraTopMenu, 0, Qt.AlignmentFlag.AlignTop)

        self.extraCenter = QFrame(self.extraContent)
        self.extraCenter.setObjectName(u"extraCenter")
        self.extraCenter.setFrameShape(QFrame.Shape.NoFrame)
        self.extraCenter.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_10 = QVBoxLayout(self.extraCenter)
        self.verticalLayout_10.setObjectName(u"verticalLayout_10")
        self.verticalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.peer = QTableWidget(self.extraCenter)
        if (self.peer.columnCount() < 1):
            self.peer.setColumnCount(1)
        __qtablewidgetitem = QTableWidgetItem()
        self.peer.setHorizontalHeaderItem(0, __qtablewidgetitem)
        if (self.peer.rowCount() < 13):
            self.peer.setRowCount(13)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setTextAlignment(Qt.AlignCenter);
        self.peer.setVerticalHeaderItem(0, __qtablewidgetitem1)
        __qtablewidgetitem2 = QTableWidgetItem()
        self.peer.setVerticalHeaderItem(1, __qtablewidgetitem2)
        __qtablewidgetitem3 = QTableWidgetItem()
        self.peer.setVerticalHeaderItem(2, __qtablewidgetitem3)
        __qtablewidgetitem4 = QTableWidgetItem()
        self.peer.setVerticalHeaderItem(3, __qtablewidgetitem4)
        __qtablewidgetitem5 = QTableWidgetItem()
        self.peer.setVerticalHeaderItem(4, __qtablewidgetitem5)
        __qtablewidgetitem6 = QTableWidgetItem()
        self.peer.setVerticalHeaderItem(5, __qtablewidgetitem6)
        __qtablewidgetitem7 = QTableWidgetItem()
        self.peer.setVerticalHeaderItem(6, __qtablewidgetitem7)
        __qtablewidgetitem8 = QTableWidgetItem()
        self.peer.setVerticalHeaderItem(7, __qtablewidgetitem8)
        __qtablewidgetitem9 = QTableWidgetItem()
        self.peer.setVerticalHeaderItem(8, __qtablewidgetitem9)
        __qtablewidgetitem10 = QTableWidgetItem()
        self.peer.setVerticalHeaderItem(9, __qtablewidgetitem10)
        __qtablewidgetitem11 = QTableWidgetItem()
        self.peer.setVerticalHeaderItem(10, __qtablewidgetitem11)
        __qtablewidgetitem12 = QTableWidgetItem()
        self.peer.setVerticalHeaderItem(11, __qtablewidgetitem12)
        __qtablewidgetitem13 = QTableWidgetItem()
        self.peer.setVerticalHeaderItem(12, __qtablewidgetitem13)
        __qtablewidgetitem14 = QTableWidgetItem()
        self.peer.setItem(0, 0, __qtablewidgetitem14)
        __qtablewidgetitem15 = QTableWidgetItem()
        self.peer.setItem(1, 0, __qtablewidgetitem15)
        __qtablewidgetitem16 = QTableWidgetItem()
        self.peer.setItem(2, 0, __qtablewidgetitem16)
        __qtablewidgetitem17 = QTableWidgetItem()
        self.peer.setItem(3, 0, __qtablewidgetitem17)
        __qtablewidgetitem18 = QTableWidgetItem()
        self.peer.setItem(4, 0, __qtablewidgetitem18)
        __qtablewidgetitem19 = QTableWidgetItem()
        self.peer.setItem(5, 0, __qtablewidgetitem19)
        __qtablewidgetitem20 = QTableWidgetItem()
        self.peer.setItem(6, 0, __qtablewidgetitem20)
        __qtablewidgetitem21 = QTableWidgetItem()
        self.peer.setItem(7, 0, __qtablewidgetitem21)
        __qtablewidgetitem22 = QTableWidgetItem()
        self.peer.setItem(8, 0, __qtablewidgetitem22)
        __qtablewidgetitem23 = QTableWidgetItem()
        self.peer.setItem(9, 0, __qtablewidgetitem23)
        __qtablewidgetitem24 = QTableWidgetItem()
        self.peer.setItem(10, 0, __qtablewidgetitem24)
        __qtablewidgetitem25 = QTableWidgetItem()
        self.peer.setItem(11, 0, __qtablewidgetitem25)
        __qtablewidgetitem26 = QTableWidgetItem()
        self.peer.setItem(12, 0, __qtablewidgetitem26)
        self.peer.setObjectName(u"peer")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy1.setHorizontalStretch(1)
        sizePolicy1.setVerticalStretch(1)
        sizePolicy1.setHeightForWidth(self.peer.sizePolicy().hasHeightForWidth())
        self.peer.setSizePolicy(sizePolicy1)
        self.peer.setStyleSheet(u"/* \u8868\u683c\u6574\u4f53\u6837\u5f0f */\n"
"QTableWidget {\n"
"    background-color: transparent;\n"
"    border: none;\n"
"    outline: none;\n"
"    font: inherit;\n"
"	font-size: 12pt;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"/* \u5355\u5143\u683c\u6837\u5f0f - \u589e\u52a0\u5bbd\u5ea6\u63a7\u5236 */\n"
"QTableWidget::item {\n"
" \n"
"    background-color: transparent;\n"
"\n"
"}\n"
"")
        self.peer.setAlternatingRowColors(True)
        self.peer.setShowGrid(False)
        self.peer.horizontalHeader().setVisible(False)
        self.peer.horizontalHeader().setStretchLastSection(True)
        self.peer.verticalHeader().setVisible(False)
        self.peer.verticalHeader().setDefaultSectionSize(60)

        self.verticalLayout_10.addWidget(self.peer)


        self.verticalLayout_12.addWidget(self.extraCenter)

        self.extraBottom = QFrame(self.extraContent)
        self.extraBottom.setObjectName(u"extraBottom")
        self.extraBottom.setFrameShape(QFrame.Shape.NoFrame)
        self.extraBottom.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_12.addWidget(self.extraBottom)


        self.extraColumLayout.addWidget(self.extraContent)


        self.appLayout.addWidget(self.extraLeftBox)

        self.contentBox = QFrame(self.bgApp)
        self.contentBox.setObjectName(u"contentBox")
        self.contentBox.setFrameShape(QFrame.Shape.NoFrame)
        self.contentBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_2 = QVBoxLayout(self.contentBox)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.contentTopBg = QFrame(self.contentBox)
        self.contentTopBg.setObjectName(u"contentTopBg")
        self.contentTopBg.setMinimumSize(QSize(0, 50))
        self.contentTopBg.setMaximumSize(QSize(16777215, 50))
        self.contentTopBg.setFrameShape(QFrame.Shape.NoFrame)
        self.contentTopBg.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout = QHBoxLayout(self.contentTopBg)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.horizontalLayout.setContentsMargins(0, 0, 10, 0)
        self.leftBox = QFrame(self.contentTopBg)
        self.leftBox.setObjectName(u"leftBox")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        sizePolicy2.setHorizontalStretch(0)
        sizePolicy2.setVerticalStretch(0)
        sizePolicy2.setHeightForWidth(self.leftBox.sizePolicy().hasHeightForWidth())
        self.leftBox.setSizePolicy(sizePolicy2)
        self.leftBox.setFrameShape(QFrame.Shape.NoFrame)
        self.leftBox.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_3 = QHBoxLayout(self.leftBox)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName(u"horizontalLayout_3")
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.titleRightInfo = QLabel(self.leftBox)
        self.titleRightInfo.setObjectName(u"titleRightInfo")
        sizePolicy3 = QSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)
        sizePolicy3.setHorizontalStretch(0)
        sizePolicy3.setVerticalStretch(0)
        sizePolicy3.setHeightForWidth(self.titleRightInfo.sizePolicy().hasHeightForWidth())
        self.titleRightInfo.setSizePolicy(sizePolicy3)
        self.titleRightInfo.setMaximumSize(QSize(16777215, 45))
        self.titleRightInfo.setFont(font)
        self.titleRightInfo.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_3.addWidget(self.titleRightInfo)


        self.horizontalLayout.addWidget(self.leftBox)

        self.rightButtons = QFrame(self.contentTopBg)
        self.rightButtons.setObjectName(u"rightButtons")
        self.rightButtons.setMinimumSize(QSize(0, 28))
        self.rightButtons.setFrameShape(QFrame.Shape.NoFrame)
        self.rightButtons.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_2 = QHBoxLayout(self.rightButtons)
        self.horizontalLayout_2.setSpacing(5)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.minimizeAppBtn = QPushButton(self.rightButtons)
        self.minimizeAppBtn.setObjectName(u"minimizeAppBtn")
        self.minimizeAppBtn.setMinimumSize(QSize(28, 28))
        self.minimizeAppBtn.setMaximumSize(QSize(28, 28))
        self.minimizeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon2 = QIcon()
        icon2.addFile(u":/icons/icons/icon_minimize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.minimizeAppBtn.setIcon(icon2)
        self.minimizeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.minimizeAppBtn)

        self.maximizeRestoreAppBtn = QPushButton(self.rightButtons)
        self.maximizeRestoreAppBtn.setObjectName(u"maximizeRestoreAppBtn")
        self.maximizeRestoreAppBtn.setMinimumSize(QSize(28, 28))
        self.maximizeRestoreAppBtn.setMaximumSize(QSize(28, 28))
        font1 = QFont()
        font1.setFamilies([u"Segoe UI"])
        font1.setPointSize(10)
        font1.setBold(False)
        font1.setItalic(False)
        font1.setStyleStrategy(QFont.PreferDefault)
        self.maximizeRestoreAppBtn.setFont(font1)
        self.maximizeRestoreAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        icon3 = QIcon()
        icon3.addFile(u":/icons/icons/icon_maximize.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.maximizeRestoreAppBtn.setIcon(icon3)
        self.maximizeRestoreAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.maximizeRestoreAppBtn)

        self.closeAppBtn = QPushButton(self.rightButtons)
        self.closeAppBtn.setObjectName(u"closeAppBtn")
        self.closeAppBtn.setMinimumSize(QSize(28, 28))
        self.closeAppBtn.setMaximumSize(QSize(28, 28))
        self.closeAppBtn.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.closeAppBtn.setIcon(icon1)
        self.closeAppBtn.setIconSize(QSize(20, 20))

        self.horizontalLayout_2.addWidget(self.closeAppBtn)


        self.horizontalLayout.addWidget(self.rightButtons, 0, Qt.AlignmentFlag.AlignRight)


        self.verticalLayout_2.addWidget(self.contentTopBg)

        self.contentBottom = QFrame(self.contentBox)
        self.contentBottom.setObjectName(u"contentBottom")
        self.contentBottom.setFrameShape(QFrame.Shape.NoFrame)
        self.contentBottom.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_6 = QVBoxLayout(self.contentBottom)
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setObjectName(u"verticalLayout_6")
        self.verticalLayout_6.setContentsMargins(0, 0, 0, 0)
        self.content = QFrame(self.contentBottom)
        self.content.setObjectName(u"content")
        self.content.setFrameShape(QFrame.Shape.NoFrame)
        self.content.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_4 = QHBoxLayout(self.content)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName(u"horizontalLayout_4")
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.pagesContainer = QFrame(self.content)
        self.pagesContainer.setObjectName(u"pagesContainer")
        self.pagesContainer.setStyleSheet(u"")
        self.pagesContainer.setFrameShape(QFrame.Shape.NoFrame)
        self.pagesContainer.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_15 = QVBoxLayout(self.pagesContainer)
        self.verticalLayout_15.setSpacing(0)
        self.verticalLayout_15.setObjectName(u"verticalLayout_15")
        self.verticalLayout_15.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget = QStackedWidget(self.pagesContainer)
        self.stackedWidget.setObjectName(u"stackedWidget")
        self.stackedWidget.setStyleSheet(u"background: transparent;")
        self.home = QWidget()
        self.home.setObjectName(u"home")
        self.home.setStyleSheet(u"background-image: url(:/images/images/MNS.png);\n"
"background-position: center;\n"
"background-repeat: no-repeat;\n"
"")
        self.stackedWidget.addWidget(self.home)
        self.widgets = QWidget()
        self.widgets.setObjectName(u"widgets")
        self.widgets.setStyleSheet(u"b")
        self.verticalLayout = QVBoxLayout(self.widgets)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(10, 10, 10, 10)
        self.stackedWidget.addWidget(self.widgets)
        self.FileCheck = QWidget()
        self.FileCheck.setObjectName(u"FileCheck")
        self.verticalLayout_20 = QVBoxLayout(self.FileCheck)
        self.verticalLayout_20.setSpacing(0)
        self.verticalLayout_20.setObjectName(u"verticalLayout_20")
        self.verticalLayout_20.setContentsMargins(0, 0, 0, 0)
        self.gridFrame = QFrame(self.FileCheck)
        self.gridFrame.setObjectName(u"gridFrame")
        self.horizontalLayout_14 = QHBoxLayout(self.gridFrame)
        self.horizontalLayout_14.setObjectName(u"horizontalLayout_14")
        self.horizontalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.horizontalFrame = QFrame(self.gridFrame)
        self.horizontalFrame.setObjectName(u"horizontalFrame")
        self.verticalLayout_26 = QVBoxLayout(self.horizontalFrame)
        self.verticalLayout_26.setObjectName(u"verticalLayout_26")
        self.LocalFile = QFrame(self.horizontalFrame)
        self.LocalFile.setObjectName(u"LocalFile")
        self.verticalLayout_27 = QVBoxLayout(self.LocalFile)
        self.verticalLayout_27.setObjectName(u"verticalLayout_27")
        self.verticalLayout_27.setContentsMargins(0, 0, 0, 0)
        self.pushButton_2 = QPushButton(self.LocalFile)
        self.pushButton_2.setObjectName(u"pushButton_2")
        self.pushButton_2.setStyleSheet(u"QPushButton {\n"
"    background-color: transparent;\n"
"    color: palette(link);\n"
"    border: none;\n"
"    padding: 0.3em 0.6em;\n"
"    font: inherit;\n"
"	text-align : left;\n"
"	font-size: 12pt;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton :hover {\n"
"    background-color: palette(light);\n"
"    border-radius: 0.2em;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: palette(mid);\n"
"}")

        self.verticalLayout_27.addWidget(self.pushButton_2)

        self.tableWidget_2 = DraggableTableWidget(self.LocalFile)
        if (self.tableWidget_2.columnCount() < 3):
            self.tableWidget_2.setColumnCount(3)
        __qtablewidgetitem27 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, __qtablewidgetitem27)
        __qtablewidgetitem28 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, __qtablewidgetitem28)
        __qtablewidgetitem29 = QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, __qtablewidgetitem29)
        if (self.tableWidget_2.rowCount() < 20):
            self.tableWidget_2.setRowCount(20)
        __qtablewidgetitem30 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(0, __qtablewidgetitem30)
        __qtablewidgetitem31 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(1, __qtablewidgetitem31)
        __qtablewidgetitem32 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(2, __qtablewidgetitem32)
        __qtablewidgetitem33 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(3, __qtablewidgetitem33)
        __qtablewidgetitem34 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(4, __qtablewidgetitem34)
        __qtablewidgetitem35 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(5, __qtablewidgetitem35)
        __qtablewidgetitem36 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(6, __qtablewidgetitem36)
        __qtablewidgetitem37 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(7, __qtablewidgetitem37)
        __qtablewidgetitem38 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(8, __qtablewidgetitem38)
        __qtablewidgetitem39 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(9, __qtablewidgetitem39)
        __qtablewidgetitem40 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(10, __qtablewidgetitem40)
        __qtablewidgetitem41 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(11, __qtablewidgetitem41)
        __qtablewidgetitem42 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(12, __qtablewidgetitem42)
        __qtablewidgetitem43 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(13, __qtablewidgetitem43)
        __qtablewidgetitem44 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(14, __qtablewidgetitem44)
        __qtablewidgetitem45 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(15, __qtablewidgetitem45)
        __qtablewidgetitem46 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(16, __qtablewidgetitem46)
        __qtablewidgetitem47 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(17, __qtablewidgetitem47)
        __qtablewidgetitem48 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(18, __qtablewidgetitem48)
        __qtablewidgetitem49 = QTableWidgetItem()
        self.tableWidget_2.setVerticalHeaderItem(19, __qtablewidgetitem49)
        __qtablewidgetitem50 = QTableWidgetItem()
        self.tableWidget_2.setItem(0, 0, __qtablewidgetitem50)
        __qtablewidgetitem51 = QTableWidgetItem()
        self.tableWidget_2.setItem(0, 1, __qtablewidgetitem51)
        __qtablewidgetitem52 = QTableWidgetItem()
        self.tableWidget_2.setItem(0, 2, __qtablewidgetitem52)
        __qtablewidgetitem53 = QTableWidgetItem()
        self.tableWidget_2.setItem(1, 0, __qtablewidgetitem53)
        __qtablewidgetitem54 = QTableWidgetItem()
        self.tableWidget_2.setItem(1, 1, __qtablewidgetitem54)
        __qtablewidgetitem55 = QTableWidgetItem()
        self.tableWidget_2.setItem(1, 2, __qtablewidgetitem55)
        __qtablewidgetitem56 = QTableWidgetItem()
        self.tableWidget_2.setItem(2, 0, __qtablewidgetitem56)
        __qtablewidgetitem57 = QTableWidgetItem()
        self.tableWidget_2.setItem(2, 1, __qtablewidgetitem57)
        __qtablewidgetitem58 = QTableWidgetItem()
        self.tableWidget_2.setItem(2, 2, __qtablewidgetitem58)
        __qtablewidgetitem59 = QTableWidgetItem()
        self.tableWidget_2.setItem(3, 0, __qtablewidgetitem59)
        __qtablewidgetitem60 = QTableWidgetItem()
        self.tableWidget_2.setItem(3, 1, __qtablewidgetitem60)
        __qtablewidgetitem61 = QTableWidgetItem()
        self.tableWidget_2.setItem(3, 2, __qtablewidgetitem61)
        __qtablewidgetitem62 = QTableWidgetItem()
        self.tableWidget_2.setItem(4, 0, __qtablewidgetitem62)
        __qtablewidgetitem63 = QTableWidgetItem()
        self.tableWidget_2.setItem(4, 1, __qtablewidgetitem63)
        __qtablewidgetitem64 = QTableWidgetItem()
        self.tableWidget_2.setItem(4, 2, __qtablewidgetitem64)
        __qtablewidgetitem65 = QTableWidgetItem()
        self.tableWidget_2.setItem(5, 0, __qtablewidgetitem65)
        __qtablewidgetitem66 = QTableWidgetItem()
        self.tableWidget_2.setItem(5, 1, __qtablewidgetitem66)
        __qtablewidgetitem67 = QTableWidgetItem()
        self.tableWidget_2.setItem(5, 2, __qtablewidgetitem67)
        __qtablewidgetitem68 = QTableWidgetItem()
        self.tableWidget_2.setItem(6, 0, __qtablewidgetitem68)
        __qtablewidgetitem69 = QTableWidgetItem()
        self.tableWidget_2.setItem(6, 1, __qtablewidgetitem69)
        __qtablewidgetitem70 = QTableWidgetItem()
        self.tableWidget_2.setItem(6, 2, __qtablewidgetitem70)
        __qtablewidgetitem71 = QTableWidgetItem()
        self.tableWidget_2.setItem(13, 0, __qtablewidgetitem71)
        __qtablewidgetitem72 = QTableWidgetItem()
        self.tableWidget_2.setItem(13, 2, __qtablewidgetitem72)
        __qtablewidgetitem73 = QTableWidgetItem()
        self.tableWidget_2.setItem(14, 0, __qtablewidgetitem73)
        __qtablewidgetitem74 = QTableWidgetItem()
        self.tableWidget_2.setItem(14, 2, __qtablewidgetitem74)
        __qtablewidgetitem75 = QTableWidgetItem()
        self.tableWidget_2.setItem(15, 0, __qtablewidgetitem75)
        __qtablewidgetitem76 = QTableWidgetItem()
        self.tableWidget_2.setItem(15, 2, __qtablewidgetitem76)
        __qtablewidgetitem77 = QTableWidgetItem()
        self.tableWidget_2.setItem(17, 0, __qtablewidgetitem77)
        __qtablewidgetitem78 = QTableWidgetItem()
        self.tableWidget_2.setItem(17, 2, __qtablewidgetitem78)
        __qtablewidgetitem79 = QTableWidgetItem()
        self.tableWidget_2.setItem(18, 0, __qtablewidgetitem79)
        self.tableWidget_2.setObjectName(u"tableWidget_2")
        self.tableWidget_2.setAcceptDrops(True)
        self.tableWidget_2.setStyleSheet(u"/* \u4f7f\u7528\u7cfb\u7edf\u989c\u8272\u548c\u76f8\u5bf9\u5355\u4f4d */\n"
"QTableWidget {\n"
"    background-color: palette(base);\n"
"    gridline-color: palette(mid);\n"
"    border: 1px solid palette(mid);\n"
"    alternate-background-color: palette(alternate-base);\n"
"    font: inherit; /* \u7ee7\u627f\u7cfb\u7edf\u5b57\u4f53\u8bbe\u7f6e */\n"
"	gridline-color: transparent;\n"
"	show-decoration-selected: 1;\n"
"}\n"
"\n"
"/* \u8868\u5934\u6837\u5f0f - \u4f7f\u7528\u7cfb\u7edf\u8c03\u8272\u677f */\n"
"QHeaderView::section {\n"
"    background-color: palette(button);\n"
"    border-left: none;\n"
"    padding: 0.2em; /* \u4f7f\u7528\u76f8\u5bf9\u5355\u4f4d em */\n"
"    font-weight: bold;\n"
"    color: palette(text);\n"
"    min-height: 1.5em; /* \u76f8\u5bf9\u9ad8\u5ea6 */\n"
"	border: none; /* \u8868\u5934\u65e0\u8fb9\u6846 */\n"
"}\n"
"\n"
"/* \u8868\u683c\u5185\u5bb9\u9879\u6837\u5f0f */\n"
"QTableWidget::item {\n"
"    padding: 0.1em 0.3em; /* \u4e0a\u4e0b/\u5de6\u53f3\u5185\u8fb9\u8ddd */\n"
"}\n"
""
                        "\n"
"/* \u9009\u4e2d\u9879\u6837\u5f0f */\n"
"QTableWidget::item:selected {\n"
"    background-color: palette(highlight);\n"
"    color: palette(highlighted-text);\n"
"}\n"
"\n"
"/* \u89d2\u90e8\u6309\u94ae */\n"
"QTableCornerButton::section {\n"
"    background-color: palette(button);\n"
"    border: 1px solid palette(mid);\n"
"    border-top: none;\n"
"    border-left: none;\n"
"}\n"
"")
        self.tableWidget_2.setDragEnabled(True)
        self.tableWidget_2.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.tableWidget_2.setDefaultDropAction(Qt.DropAction.TargetMoveAction)
        self.tableWidget_2.setAlternatingRowColors(True)
        self.tableWidget_2.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tableWidget_2.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_2.horizontalHeader().setVisible(True)
        self.tableWidget_2.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_2.horizontalHeader().setMinimumSectionSize(35)
        self.tableWidget_2.horizontalHeader().setDefaultSectionSize(160)
        self.tableWidget_2.horizontalHeader().setHighlightSections(True)
        self.tableWidget_2.horizontalHeader().setProperty(u"showSortIndicator", False)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_2.verticalHeader().setVisible(False)
        self.tableWidget_2.verticalHeader().setCascadingSectionResizes(False)

        self.verticalLayout_27.addWidget(self.tableWidget_2)


        self.verticalLayout_26.addWidget(self.LocalFile)

        self.Sharing = QFrame(self.horizontalFrame)
        self.Sharing.setObjectName(u"Sharing")
        self.FileSharing = QVBoxLayout(self.Sharing)
        self.FileSharing.setObjectName(u"FileSharing")
        self.FileSharingLabel = QPushButton(self.Sharing)
        self.FileSharingLabel.setObjectName(u"FileSharingLabel")
        self.FileSharingLabel.setStyleSheet(u"QPushButton {\n"
"    background-color: transparent;\n"
"    color: palette(link);\n"
"    border: none;\n"
"    padding: 0.3em 0.6em;\n"
"    font: inherit;\n"
"	text-align : left;\n"
"	font-size: 12pt;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton :hover {\n"
"    background-color: palette(light);\n"
"    border-radius: 0.2em;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: palette(mid);\n"
"}")

        self.FileSharing.addWidget(self.FileSharingLabel)

        self.tableWidget_3 = DraggableTableWidget(self.Sharing)
        if (self.tableWidget_3.columnCount() < 3):
            self.tableWidget_3.setColumnCount(3)
        __qtablewidgetitem80 = QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(0, __qtablewidgetitem80)
        __qtablewidgetitem81 = QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(1, __qtablewidgetitem81)
        __qtablewidgetitem82 = QTableWidgetItem()
        self.tableWidget_3.setHorizontalHeaderItem(2, __qtablewidgetitem82)
        if (self.tableWidget_3.rowCount() < 21):
            self.tableWidget_3.setRowCount(21)
        __qtablewidgetitem83 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(0, __qtablewidgetitem83)
        __qtablewidgetitem84 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(1, __qtablewidgetitem84)
        __qtablewidgetitem85 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(2, __qtablewidgetitem85)
        __qtablewidgetitem86 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(3, __qtablewidgetitem86)
        __qtablewidgetitem87 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(4, __qtablewidgetitem87)
        __qtablewidgetitem88 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(5, __qtablewidgetitem88)
        __qtablewidgetitem89 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(6, __qtablewidgetitem89)
        __qtablewidgetitem90 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(7, __qtablewidgetitem90)
        __qtablewidgetitem91 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(8, __qtablewidgetitem91)
        __qtablewidgetitem92 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(9, __qtablewidgetitem92)
        __qtablewidgetitem93 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(10, __qtablewidgetitem93)
        __qtablewidgetitem94 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(11, __qtablewidgetitem94)
        __qtablewidgetitem95 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(12, __qtablewidgetitem95)
        __qtablewidgetitem96 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(13, __qtablewidgetitem96)
        __qtablewidgetitem97 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(14, __qtablewidgetitem97)
        __qtablewidgetitem98 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(15, __qtablewidgetitem98)
        __qtablewidgetitem99 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(16, __qtablewidgetitem99)
        __qtablewidgetitem100 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(17, __qtablewidgetitem100)
        __qtablewidgetitem101 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(18, __qtablewidgetitem101)
        __qtablewidgetitem102 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(19, __qtablewidgetitem102)
        __qtablewidgetitem103 = QTableWidgetItem()
        self.tableWidget_3.setVerticalHeaderItem(20, __qtablewidgetitem103)
        __qtablewidgetitem104 = QTableWidgetItem()
        self.tableWidget_3.setItem(0, 0, __qtablewidgetitem104)
        __qtablewidgetitem105 = QTableWidgetItem()
        self.tableWidget_3.setItem(0, 1, __qtablewidgetitem105)
        __qtablewidgetitem106 = QTableWidgetItem()
        self.tableWidget_3.setItem(0, 2, __qtablewidgetitem106)
        __qtablewidgetitem107 = QTableWidgetItem()
        self.tableWidget_3.setItem(1, 0, __qtablewidgetitem107)
        __qtablewidgetitem108 = QTableWidgetItem()
        self.tableWidget_3.setItem(1, 1, __qtablewidgetitem108)
        __qtablewidgetitem109 = QTableWidgetItem()
        self.tableWidget_3.setItem(1, 2, __qtablewidgetitem109)
        __qtablewidgetitem110 = QTableWidgetItem()
        self.tableWidget_3.setItem(2, 0, __qtablewidgetitem110)
        __qtablewidgetitem111 = QTableWidgetItem()
        self.tableWidget_3.setItem(2, 1, __qtablewidgetitem111)
        __qtablewidgetitem112 = QTableWidgetItem()
        self.tableWidget_3.setItem(2, 2, __qtablewidgetitem112)
        __qtablewidgetitem113 = QTableWidgetItem()
        self.tableWidget_3.setItem(3, 0, __qtablewidgetitem113)
        __qtablewidgetitem114 = QTableWidgetItem()
        self.tableWidget_3.setItem(3, 1, __qtablewidgetitem114)
        __qtablewidgetitem115 = QTableWidgetItem()
        self.tableWidget_3.setItem(3, 2, __qtablewidgetitem115)
        __qtablewidgetitem116 = QTableWidgetItem()
        self.tableWidget_3.setItem(4, 0, __qtablewidgetitem116)
        __qtablewidgetitem117 = QTableWidgetItem()
        self.tableWidget_3.setItem(4, 1, __qtablewidgetitem117)
        __qtablewidgetitem118 = QTableWidgetItem()
        self.tableWidget_3.setItem(4, 2, __qtablewidgetitem118)
        __qtablewidgetitem119 = QTableWidgetItem()
        self.tableWidget_3.setItem(5, 0, __qtablewidgetitem119)
        __qtablewidgetitem120 = QTableWidgetItem()
        self.tableWidget_3.setItem(5, 1, __qtablewidgetitem120)
        __qtablewidgetitem121 = QTableWidgetItem()
        self.tableWidget_3.setItem(5, 2, __qtablewidgetitem121)
        __qtablewidgetitem122 = QTableWidgetItem()
        self.tableWidget_3.setItem(6, 0, __qtablewidgetitem122)
        __qtablewidgetitem123 = QTableWidgetItem()
        self.tableWidget_3.setItem(6, 1, __qtablewidgetitem123)
        __qtablewidgetitem124 = QTableWidgetItem()
        self.tableWidget_3.setItem(6, 2, __qtablewidgetitem124)
        __qtablewidgetitem125 = QTableWidgetItem()
        self.tableWidget_3.setItem(7, 0, __qtablewidgetitem125)
        __qtablewidgetitem126 = QTableWidgetItem()
        self.tableWidget_3.setItem(8, 0, __qtablewidgetitem126)
        __qtablewidgetitem127 = QTableWidgetItem()
        self.tableWidget_3.setItem(9, 0, __qtablewidgetitem127)
        __qtablewidgetitem128 = QTableWidgetItem()
        self.tableWidget_3.setItem(9, 2, __qtablewidgetitem128)
        __qtablewidgetitem129 = QTableWidgetItem()
        self.tableWidget_3.setItem(10, 0, __qtablewidgetitem129)
        __qtablewidgetitem130 = QTableWidgetItem()
        self.tableWidget_3.setItem(11, 1, __qtablewidgetitem130)
        __qtablewidgetitem131 = QTableWidgetItem()
        self.tableWidget_3.setItem(12, 0, __qtablewidgetitem131)
        __qtablewidgetitem132 = QTableWidgetItem()
        self.tableWidget_3.setItem(13, 1, __qtablewidgetitem132)
        __qtablewidgetitem133 = QTableWidgetItem()
        self.tableWidget_3.setItem(13, 2, __qtablewidgetitem133)
        self.tableWidget_3.setObjectName(u"tableWidget_3")
        self.tableWidget_3.setAcceptDrops(True)
        self.tableWidget_3.setStyleSheet(u"/* \u4f7f\u7528\u7cfb\u7edf\u989c\u8272\u548c\u76f8\u5bf9\u5355\u4f4d */\n"
"QTableWidget {\n"
"    background-color: palette(base);\n"
"    gridline-color: palette(mid);\n"
"    border: 1px solid palette(mid);\n"
"    alternate-background-color: palette(alternate-base);\n"
"    font: inherit; /* \u7ee7\u627f\u7cfb\u7edf\u5b57\u4f53\u8bbe\u7f6e */\n"
"	gridline-color: transparent;\n"
"	show-decoration-selected: 1;\n"
"}\n"
"\n"
"/* \u8868\u5934\u6837\u5f0f - \u4f7f\u7528\u7cfb\u7edf\u8c03\u8272\u677f */\n"
"QHeaderView::section {\n"
"    background-color: palette(button);\n"
"    border-left: none;\n"
"    padding: 0.2em; /* \u4f7f\u7528\u76f8\u5bf9\u5355\u4f4d em */\n"
"    font-weight: bold;\n"
"    color: palette(text);\n"
"    min-height: 1.5em; /* \u76f8\u5bf9\u9ad8\u5ea6 */\n"
"	border: none; /* \u8868\u5934\u65e0\u8fb9\u6846 */\n"
"}\n"
"\n"
"/* \u8868\u683c\u5185\u5bb9\u9879\u6837\u5f0f */\n"
"QTableWidget::item {\n"
"    padding: 0.1em 0.3em; /* \u4e0a\u4e0b/\u5de6\u53f3\u5185\u8fb9\u8ddd */\n"
"}\n"
""
                        "\n"
"/* \u9009\u4e2d\u9879\u6837\u5f0f */\n"
"QTableWidget::item:selected {\n"
"    background-color: palette(highlight);\n"
"    color: palette(highlighted-text);\n"
"}\n"
"\n"
"/* \u89d2\u90e8\u6309\u94ae */\n"
"QTableCornerButton::section {\n"
"    background-color: palette(button);\n"
"    border: 1px solid palette(mid);\n"
"    border-top: none;\n"
"    border-left: none;\n"
"}\n"
"")
        self.tableWidget_3.setDragEnabled(True)
        self.tableWidget_3.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.tableWidget_3.setAlternatingRowColors(True)
        self.tableWidget_3.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.tableWidget_3.horizontalHeader().setDefaultSectionSize(160)
        self.tableWidget_3.horizontalHeader().setStretchLastSection(True)
        self.tableWidget_3.verticalHeader().setVisible(False)

        self.FileSharing.addWidget(self.tableWidget_3)


        self.verticalLayout_26.addWidget(self.Sharing)


        self.horizontalLayout_14.addWidget(self.horizontalFrame)

        self.peerDocument = QFrame(self.gridFrame)
        self.peerDocument.setObjectName(u"peerDocument")
        self.verticalLayout_30 = QVBoxLayout(self.peerDocument)
        self.verticalLayout_30.setObjectName(u"verticalLayout_30")
        self.horizontalFrame_5 = QFrame(self.peerDocument)
        self.horizontalFrame_5.setObjectName(u"horizontalFrame_5")
        self.horizontalFrame_5.setMinimumSize(QSize(0, 24))
        self.verticalLayout_18 = QVBoxLayout(self.horizontalFrame_5)
        self.verticalLayout_18.setObjectName(u"verticalLayout_18")
        self.verticalLayout_18.setContentsMargins(0, 0, 0, 0)
        self.horizontalFrame_6 = QFrame(self.horizontalFrame_5)
        self.horizontalFrame_6.setObjectName(u"horizontalFrame_6")
        self.horizontalFrame_6.setMinimumSize(QSize(0, 23))
        self.horizontalLayout_10 = QHBoxLayout(self.horizontalFrame_6)
        self.horizontalLayout_10.setObjectName(u"horizontalLayout_10")
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.HostLabel = QLabel(self.horizontalFrame_6)
        self.HostLabel.setObjectName(u"HostLabel")
        self.HostLabel.setStyleSheet(u"QLabel {\n"
"    background-color: transparent;\n"
"    color: palette(link);\n"
"    border: none;\n"
"    padding: 0.1em 0.3em;\n"
"    font: inherit;\n"
"	text-align : center;\n"
"	font-size: 12pt;\n"
"    font-weight: bold;\n"
"}\n"
"")
        self.HostLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)
        self.HostLabel.setIndent(0)

        self.horizontalLayout_10.addWidget(self.HostLabel)

        self.horizontalLayout_10.setStretch(0, 1)

        self.verticalLayout_18.addWidget(self.horizontalFrame_6)

        self.pushButton_3 = QPushButton(self.horizontalFrame_5)
        self.pushButton_3.setObjectName(u"pushButton_3")
        self.pushButton_3.setStyleSheet(u"QPushButton {\n"
"    background-color: transparent;\n"
"    color: palette(link);\n"
"    border: none;\n"
"    padding: 0.3em 0.3em;\n"
"    font: inherit;\n"
"	text-align : left;\n"
"	font-size: 12pt;\n"
"    font-weight: bold;\n"
"}\n"
"QPushButton :hover {\n"
"    background-color: palette(light);\n"
"    border-radius: 0.2em;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: palette(mid);\n"
"}")

        self.verticalLayout_18.addWidget(self.pushButton_3)


        self.verticalLayout_30.addWidget(self.horizontalFrame_5)

        self.PeerLabel = DraggableTableWidget(self.peerDocument)
        if (self.PeerLabel.columnCount() < 3):
            self.PeerLabel.setColumnCount(3)
        __qtablewidgetitem134 = QTableWidgetItem()
        self.PeerLabel.setHorizontalHeaderItem(0, __qtablewidgetitem134)
        __qtablewidgetitem135 = QTableWidgetItem()
        self.PeerLabel.setHorizontalHeaderItem(1, __qtablewidgetitem135)
        __qtablewidgetitem136 = QTableWidgetItem()
        self.PeerLabel.setHorizontalHeaderItem(2, __qtablewidgetitem136)
        if (self.PeerLabel.rowCount() < 21):
            self.PeerLabel.setRowCount(21)
        __qtablewidgetitem137 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(0, __qtablewidgetitem137)
        __qtablewidgetitem138 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(1, __qtablewidgetitem138)
        __qtablewidgetitem139 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(2, __qtablewidgetitem139)
        __qtablewidgetitem140 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(3, __qtablewidgetitem140)
        __qtablewidgetitem141 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(4, __qtablewidgetitem141)
        __qtablewidgetitem142 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(5, __qtablewidgetitem142)
        __qtablewidgetitem143 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(6, __qtablewidgetitem143)
        __qtablewidgetitem144 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(7, __qtablewidgetitem144)
        __qtablewidgetitem145 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(8, __qtablewidgetitem145)
        __qtablewidgetitem146 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(9, __qtablewidgetitem146)
        __qtablewidgetitem147 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(10, __qtablewidgetitem147)
        __qtablewidgetitem148 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(11, __qtablewidgetitem148)
        __qtablewidgetitem149 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(12, __qtablewidgetitem149)
        __qtablewidgetitem150 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(13, __qtablewidgetitem150)
        __qtablewidgetitem151 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(14, __qtablewidgetitem151)
        __qtablewidgetitem152 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(15, __qtablewidgetitem152)
        __qtablewidgetitem153 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(16, __qtablewidgetitem153)
        __qtablewidgetitem154 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(17, __qtablewidgetitem154)
        __qtablewidgetitem155 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(18, __qtablewidgetitem155)
        __qtablewidgetitem156 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(19, __qtablewidgetitem156)
        __qtablewidgetitem157 = QTableWidgetItem()
        self.PeerLabel.setVerticalHeaderItem(20, __qtablewidgetitem157)
        __qtablewidgetitem158 = QTableWidgetItem()
        self.PeerLabel.setItem(0, 0, __qtablewidgetitem158)
        __qtablewidgetitem159 = QTableWidgetItem()
        self.PeerLabel.setItem(0, 1, __qtablewidgetitem159)
        __qtablewidgetitem160 = QTableWidgetItem()
        self.PeerLabel.setItem(0, 2, __qtablewidgetitem160)
        __qtablewidgetitem161 = QTableWidgetItem()
        self.PeerLabel.setItem(1, 0, __qtablewidgetitem161)
        __qtablewidgetitem162 = QTableWidgetItem()
        self.PeerLabel.setItem(1, 1, __qtablewidgetitem162)
        __qtablewidgetitem163 = QTableWidgetItem()
        self.PeerLabel.setItem(2, 2, __qtablewidgetitem163)
        __qtablewidgetitem164 = QTableWidgetItem()
        self.PeerLabel.setItem(3, 0, __qtablewidgetitem164)
        __qtablewidgetitem165 = QTableWidgetItem()
        self.PeerLabel.setItem(3, 1, __qtablewidgetitem165)
        __qtablewidgetitem166 = QTableWidgetItem()
        self.PeerLabel.setItem(4, 0, __qtablewidgetitem166)
        __qtablewidgetitem167 = QTableWidgetItem()
        self.PeerLabel.setItem(5, 1, __qtablewidgetitem167)
        __qtablewidgetitem168 = QTableWidgetItem()
        self.PeerLabel.setItem(5, 2, __qtablewidgetitem168)
        __qtablewidgetitem169 = QTableWidgetItem()
        self.PeerLabel.setItem(6, 0, __qtablewidgetitem169)
        __qtablewidgetitem170 = QTableWidgetItem()
        self.PeerLabel.setItem(13, 0, __qtablewidgetitem170)
        __qtablewidgetitem171 = QTableWidgetItem()
        self.PeerLabel.setItem(13, 1, __qtablewidgetitem171)
        __qtablewidgetitem172 = QTableWidgetItem()
        self.PeerLabel.setItem(13, 2, __qtablewidgetitem172)
        __qtablewidgetitem173 = QTableWidgetItem()
        self.PeerLabel.setItem(14, 0, __qtablewidgetitem173)
        __qtablewidgetitem174 = QTableWidgetItem()
        self.PeerLabel.setItem(14, 1, __qtablewidgetitem174)
        __qtablewidgetitem175 = QTableWidgetItem()
        self.PeerLabel.setItem(14, 2, __qtablewidgetitem175)
        __qtablewidgetitem176 = QTableWidgetItem()
        self.PeerLabel.setItem(15, 0, __qtablewidgetitem176)
        __qtablewidgetitem177 = QTableWidgetItem()
        self.PeerLabel.setItem(15, 1, __qtablewidgetitem177)
        __qtablewidgetitem178 = QTableWidgetItem()
        self.PeerLabel.setItem(15, 2, __qtablewidgetitem178)
        __qtablewidgetitem179 = QTableWidgetItem()
        self.PeerLabel.setItem(16, 0, __qtablewidgetitem179)
        __qtablewidgetitem180 = QTableWidgetItem()
        self.PeerLabel.setItem(17, 0, __qtablewidgetitem180)
        __qtablewidgetitem181 = QTableWidgetItem()
        self.PeerLabel.setItem(18, 1, __qtablewidgetitem181)
        __qtablewidgetitem182 = QTableWidgetItem()
        self.PeerLabel.setItem(19, 0, __qtablewidgetitem182)
        __qtablewidgetitem183 = QTableWidgetItem()
        self.PeerLabel.setItem(19, 1, __qtablewidgetitem183)
        __qtablewidgetitem184 = QTableWidgetItem()
        self.PeerLabel.setItem(20, 0, __qtablewidgetitem184)
        __qtablewidgetitem185 = QTableWidgetItem()
        self.PeerLabel.setItem(20, 1, __qtablewidgetitem185)
        self.PeerLabel.setObjectName(u"PeerLabel")
        self.PeerLabel.setAcceptDrops(True)
        self.PeerLabel.setStyleSheet(u"/* \u4f7f\u7528\u7cfb\u7edf\u989c\u8272\u548c\u76f8\u5bf9\u5355\u4f4d */\n"
"QTableWidget {\n"
"    background-color: palette(base);\n"
"    gridline-color: palette(mid);\n"
"    border: 1px solid palette(mid);\n"
"    alternate-background-color: palette(alternate-base);\n"
"    font: inherit; /* \u7ee7\u627f\u7cfb\u7edf\u5b57\u4f53\u8bbe\u7f6e */\n"
"	gridline-color: transparent;\n"
"	show-decoration-selected: 1;\n"
"}\n"
"\n"
"/* \u8868\u5934\u6837\u5f0f - \u4f7f\u7528\u7cfb\u7edf\u8c03\u8272\u677f */\n"
"QHeaderView::section {\n"
"    background-color: palette(button);\n"
"    border-left: none;\n"
"    padding: 0.2em; /* \u4f7f\u7528\u76f8\u5bf9\u5355\u4f4d em */\n"
"    font-weight: bold;\n"
"    color: palette(text);\n"
"    min-height: 1.5em; /* \u76f8\u5bf9\u9ad8\u5ea6 */\n"
"	border: none; /* \u8868\u5934\u65e0\u8fb9\u6846 */\n"
"}\n"
"\n"
"/* \u8868\u683c\u5185\u5bb9\u9879\u6837\u5f0f */\n"
"QTableWidget::item {\n"
"    padding: 0.1em 0.3em; /* \u4e0a\u4e0b/\u5de6\u53f3\u5185\u8fb9\u8ddd */\n"
"}\n"
""
                        "\n"
"/* \u9009\u4e2d\u9879\u6837\u5f0f */\n"
"QTableWidget::item:selected {\n"
"    background-color: palette(highlight);\n"
"    color: palette(highlighted-text);\n"
"}\n"
"\n"
"/* \u89d2\u90e8\u6309\u94ae */\n"
"QTableCornerButton::section {\n"
"    background-color: palette(button);\n"
"    border: 1px solid palette(mid);\n"
"    border-top: none;\n"
"    border-left: none;\n"
"}\n"
"")
        self.PeerLabel.setDragEnabled(True)
        self.PeerLabel.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop)
        self.PeerLabel.setDefaultDropAction(Qt.DropAction.LinkAction)
        self.PeerLabel.setAlternatingRowColors(True)
        self.PeerLabel.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.PeerLabel.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.PeerLabel.horizontalHeader().setDefaultSectionSize(160)
        self.PeerLabel.horizontalHeader().setStretchLastSection(True)
        self.PeerLabel.verticalHeader().setVisible(False)

        self.verticalLayout_30.addWidget(self.PeerLabel)


        self.horizontalLayout_14.addWidget(self.peerDocument)

        self.horizontalLayout_14.setStretch(0, 1)
        self.horizontalLayout_14.setStretch(1, 1)

        self.verticalLayout_20.addWidget(self.gridFrame)

        self.stackedWidget.addWidget(self.FileCheck)
        self.DownloadCheck = QWidget()
        self.DownloadCheck.setObjectName(u"DownloadCheck")
        self.verticalLayout_33 = QVBoxLayout(self.DownloadCheck)
        self.verticalLayout_33.setObjectName(u"verticalLayout_33")
        self.verticalFrame_2 = QFrame(self.DownloadCheck)
        self.verticalFrame_2.setObjectName(u"verticalFrame_2")
        self.verticalLayout_31 = QVBoxLayout(self.verticalFrame_2)
        self.verticalLayout_31.setObjectName(u"verticalLayout_31")
        self.SendingChangingButtonFrame = QFrame(self.verticalFrame_2)
        self.SendingChangingButtonFrame.setObjectName(u"SendingChangingButtonFrame")
        self.SendingChangingButtonFrame.setMinimumSize(QSize(16, 48))
        self.horizontalLayout_6 = QHBoxLayout(self.SendingChangingButtonFrame)
        self.horizontalLayout_6.setObjectName(u"horizontalLayout_6")
        self.FromLocal = QPushButton(self.SendingChangingButtonFrame)
        self.FromLocal.setObjectName(u"FromLocal")
        self.FromLocal.setMaximumSize(QSize(16777215, 16777215))
        self.FromLocal.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border: 1px solid #cccccc;\n"
"    border-bottom: none;\n"
"    font-weight: bold;\n"
"    padding: 0.4em 1.2em;  /* \u76f8\u5bf9\u5355\u4f4d */\n"
"    color: #333333;\n"
"    border-top-left-radius: 0.3em;\n"
"    border-top-right-radius: 0.3em;\n"
"}")

        self.horizontalLayout_6.addWidget(self.FromLocal)

        self.ToLocal = QPushButton(self.SendingChangingButtonFrame)
        self.ToLocal.setObjectName(u"ToLocal")
        self.ToLocal.setMaximumSize(QSize(16777215, 16777215))
        self.ToLocal.setStyleSheet(u"QPushButton {\n"
"    background-color: #f0f0f0;\n"
"    border: 1px solid #cccccc;\n"
"    border-bottom: none;\n"
"    color: #888888;\n"
"    padding: 6px 16px;\n"
"    border-top-left-radius: 5px;\n"
"    border-top-right-radius: 5px;\n"
"}")

        self.horizontalLayout_6.addWidget(self.ToLocal)

        self.label = QLabel(self.SendingChangingButtonFrame)
        self.label.setObjectName(u"label")

        self.horizontalLayout_6.addWidget(self.label)

        self.horizontalLayout_6.setStretch(0, 1)
        self.horizontalLayout_6.setStretch(1, 1)
        self.horizontalLayout_6.setStretch(2, 8)

        self.verticalLayout_31.addWidget(self.SendingChangingButtonFrame)

        self.verticalFrame_3 = QFrame(self.verticalFrame_2)
        self.verticalFrame_3.setObjectName(u"verticalFrame_3")
        self.verticalFrame_3.setMinimumSize(QSize(0, 39))
        self.verticalLayout_17 = QVBoxLayout(self.verticalFrame_3)
        self.verticalLayout_17.setObjectName(u"verticalLayout_17")
        self.verticalLayout_17.setContentsMargins(0, 0, 0, 0)
        self.sendingPage = QStackedWidget(self.verticalFrame_3)
        self.sendingPage.setObjectName(u"sendingPage")
        sizePolicy4 = QSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        sizePolicy4.setHorizontalStretch(0)
        sizePolicy4.setVerticalStretch(0)
        sizePolicy4.setHeightForWidth(self.sendingPage.sizePolicy().hasHeightForWidth())
        self.sendingPage.setSizePolicy(sizePolicy4)
        self.page = QWidget()
        self.page.setObjectName(u"page")
        self.horizontalLayout_8 = QHBoxLayout(self.page)
        self.horizontalLayout_8.setObjectName(u"horizontalLayout_8")
        self.horizontalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.FromSendingData = HoverableTable(self.page)
        if (self.FromSendingData.columnCount() < 3):
            self.FromSendingData.setColumnCount(3)
        __qtablewidgetitem186 = QTableWidgetItem()
        self.FromSendingData.setHorizontalHeaderItem(0, __qtablewidgetitem186)
        __qtablewidgetitem187 = QTableWidgetItem()
        self.FromSendingData.setHorizontalHeaderItem(1, __qtablewidgetitem187)
        __qtablewidgetitem188 = QTableWidgetItem()
        self.FromSendingData.setHorizontalHeaderItem(2, __qtablewidgetitem188)
        if (self.FromSendingData.rowCount() < 7):
            self.FromSendingData.setRowCount(7)
        __qtablewidgetitem189 = QTableWidgetItem()
        self.FromSendingData.setVerticalHeaderItem(0, __qtablewidgetitem189)
        __qtablewidgetitem190 = QTableWidgetItem()
        self.FromSendingData.setVerticalHeaderItem(1, __qtablewidgetitem190)
        __qtablewidgetitem191 = QTableWidgetItem()
        self.FromSendingData.setVerticalHeaderItem(2, __qtablewidgetitem191)
        __qtablewidgetitem192 = QTableWidgetItem()
        self.FromSendingData.setVerticalHeaderItem(3, __qtablewidgetitem192)
        __qtablewidgetitem193 = QTableWidgetItem()
        self.FromSendingData.setVerticalHeaderItem(4, __qtablewidgetitem193)
        __qtablewidgetitem194 = QTableWidgetItem()
        self.FromSendingData.setVerticalHeaderItem(5, __qtablewidgetitem194)
        __qtablewidgetitem195 = QTableWidgetItem()
        self.FromSendingData.setVerticalHeaderItem(6, __qtablewidgetitem195)
        __qtablewidgetitem196 = QTableWidgetItem()
        self.FromSendingData.setItem(0, 0, __qtablewidgetitem196)
        __qtablewidgetitem197 = QTableWidgetItem()
        self.FromSendingData.setItem(1, 2, __qtablewidgetitem197)
        __qtablewidgetitem198 = QTableWidgetItem()
        self.FromSendingData.setItem(2, 1, __qtablewidgetitem198)
        __qtablewidgetitem199 = QTableWidgetItem()
        self.FromSendingData.setItem(2, 2, __qtablewidgetitem199)
        __qtablewidgetitem200 = QTableWidgetItem()
        self.FromSendingData.setItem(3, 0, __qtablewidgetitem200)
        __qtablewidgetitem201 = QTableWidgetItem()
        self.FromSendingData.setItem(4, 2, __qtablewidgetitem201)
        __qtablewidgetitem202 = QTableWidgetItem()
        self.FromSendingData.setItem(5, 1, __qtablewidgetitem202)
        __qtablewidgetitem203 = QTableWidgetItem()
        self.FromSendingData.setItem(6, 1, __qtablewidgetitem203)
        self.FromSendingData.setObjectName(u"FromSendingData")
        self.FromSendingData.setStyleSheet(u"/* \u4f7f\u7528\u7cfb\u7edf\u989c\u8272\u548c\u76f8\u5bf9\u5355\u4f4d */\n"
"QTableWidget {\n"
"    background-color: palette(base);\n"
"    gridline-color: palette(mid);\n"
"    border: 1px solid palette(mid);\n"
"    alternate-background-color: palette(alternate-base);\n"
"    font: inherit; /* \u7ee7\u627f\u7cfb\u7edf\u5b57\u4f53\u8bbe\u7f6e */\n"
"	gridline-color: transparent;\n"
"	show-decoration-selected: 1;\n"
"}\n"
"\n"
"/* \u8868\u5934\u6837\u5f0f - \u4f7f\u7528\u7cfb\u7edf\u8c03\u8272\u677f */\n"
"QHeaderView::section {\n"
"    background-color: palette(button);\n"
"    border-left: none;\n"
"    padding: 0.2em; /* \u4f7f\u7528\u76f8\u5bf9\u5355\u4f4d em */\n"
"    font-weight: bold;\n"
"    color: palette(text);\n"
"    min-height: 1.5em; /* \u76f8\u5bf9\u9ad8\u5ea6 */\n"
"	border: none; /* \u8868\u5934\u65e0\u8fb9\u6846 */\n"
"}\n"
"\n"
"/* \u8868\u683c\u5185\u5bb9\u9879\u6837\u5f0f */\n"
"QTableWidget::item {\n"
"    padding: 0.1em 0.3em; /* \u4e0a\u4e0b/\u5de6\u53f3\u5185\u8fb9\u8ddd */\n"
"}\n"
""
                        "\n"
"/* \u9009\u4e2d\u9879\u6837\u5f0f */\n"
"QTableWidget::item:selected {\n"
"    background-color: palette(highlight);\n"
"    color: palette(highlighted-text);\n"
"}\n"
"\n"
"/* \u89d2\u90e8\u6309\u94ae */\n"
"QTableCornerButton::section {\n"
"    background-color: palette(button);\n"
"    border: 1px solid palette(mid);\n"
"    border-top: none;\n"
"    border-left: none;\n"
"}\n"
"")
        self.FromSendingData.verticalHeader().setVisible(False)

        self.horizontalLayout_8.addWidget(self.FromSendingData)

        self.sendingPage.addWidget(self.page)
        self.page_2 = QWidget()
        self.page_2.setObjectName(u"page_2")
        self.verticalLayout_22 = QVBoxLayout(self.page_2)
        self.verticalLayout_22.setObjectName(u"verticalLayout_22")
        self.verticalLayout_22.setContentsMargins(0, 0, 0, 0)
        self.verticalFrame_23 = QFrame(self.page_2)
        self.verticalFrame_23.setObjectName(u"verticalFrame_23")
        self.verticalLayout_16 = QVBoxLayout(self.verticalFrame_23)
        self.verticalLayout_16.setObjectName(u"verticalLayout_16")
        self.verticalLayout_16.setContentsMargins(0, 0, 0, 0)
        self.ToSendingData = HoverableTable(self.verticalFrame_23)
        if (self.ToSendingData.columnCount() < 3):
            self.ToSendingData.setColumnCount(3)
        __qtablewidgetitem204 = QTableWidgetItem()
        self.ToSendingData.setHorizontalHeaderItem(0, __qtablewidgetitem204)
        __qtablewidgetitem205 = QTableWidgetItem()
        self.ToSendingData.setHorizontalHeaderItem(1, __qtablewidgetitem205)
        __qtablewidgetitem206 = QTableWidgetItem()
        self.ToSendingData.setHorizontalHeaderItem(2, __qtablewidgetitem206)
        if (self.ToSendingData.rowCount() < 6):
            self.ToSendingData.setRowCount(6)
        __qtablewidgetitem207 = QTableWidgetItem()
        self.ToSendingData.setVerticalHeaderItem(0, __qtablewidgetitem207)
        __qtablewidgetitem208 = QTableWidgetItem()
        self.ToSendingData.setVerticalHeaderItem(1, __qtablewidgetitem208)
        __qtablewidgetitem209 = QTableWidgetItem()
        self.ToSendingData.setVerticalHeaderItem(2, __qtablewidgetitem209)
        __qtablewidgetitem210 = QTableWidgetItem()
        self.ToSendingData.setVerticalHeaderItem(3, __qtablewidgetitem210)
        __qtablewidgetitem211 = QTableWidgetItem()
        self.ToSendingData.setVerticalHeaderItem(4, __qtablewidgetitem211)
        __qtablewidgetitem212 = QTableWidgetItem()
        self.ToSendingData.setVerticalHeaderItem(5, __qtablewidgetitem212)
        __qtablewidgetitem213 = QTableWidgetItem()
        self.ToSendingData.setItem(0, 0, __qtablewidgetitem213)
        __qtablewidgetitem214 = QTableWidgetItem()
        self.ToSendingData.setItem(1, 0, __qtablewidgetitem214)
        __qtablewidgetitem215 = QTableWidgetItem()
        self.ToSendingData.setItem(2, 1, __qtablewidgetitem215)
        __qtablewidgetitem216 = QTableWidgetItem()
        self.ToSendingData.setItem(3, 1, __qtablewidgetitem216)
        __qtablewidgetitem217 = QTableWidgetItem()
        self.ToSendingData.setItem(4, 1, __qtablewidgetitem217)
        __qtablewidgetitem218 = QTableWidgetItem()
        self.ToSendingData.setItem(5, 1, __qtablewidgetitem218)
        __qtablewidgetitem219 = QTableWidgetItem()
        self.ToSendingData.setItem(5, 2, __qtablewidgetitem219)
        self.ToSendingData.setObjectName(u"ToSendingData")
        self.ToSendingData.setStyleSheet(u"/* \u4f7f\u7528\u7cfb\u7edf\u989c\u8272\u548c\u76f8\u5bf9\u5355\u4f4d */\n"
"QTableWidget {\n"
"    background-color: palette(base);\n"
"    gridline-color: palette(mid);\n"
"    border: 1px solid palette(mid);\n"
"    alternate-background-color: palette(alternate-base);\n"
"    font: inherit; /* \u7ee7\u627f\u7cfb\u7edf\u5b57\u4f53\u8bbe\u7f6e */\n"
"	gridline-color: transparent;\n"
"	show-decoration-selected: 1;\n"
"}\n"
"\n"
"/* \u8868\u5934\u6837\u5f0f - \u4f7f\u7528\u7cfb\u7edf\u8c03\u8272\u677f */\n"
"QHeaderView::section {\n"
"    background-color: palette(button);\n"
"    border-left: none;\n"
"    padding: 0.2em; /* \u4f7f\u7528\u76f8\u5bf9\u5355\u4f4d em */\n"
"    font-weight: bold;\n"
"    color: palette(text);\n"
"    min-height: 1.5em; /* \u76f8\u5bf9\u9ad8\u5ea6 */\n"
"	border: none; /* \u8868\u5934\u65e0\u8fb9\u6846 */\n"
"}\n"
"\n"
"/* \u8868\u683c\u5185\u5bb9\u9879\u6837\u5f0f */\n"
"QTableWidget::item {\n"
"    padding: 0.1em 0.3em; /* \u4e0a\u4e0b/\u5de6\u53f3\u5185\u8fb9\u8ddd */\n"
"}\n"
""
                        "\n"
"/* \u9009\u4e2d\u9879\u6837\u5f0f */\n"
"QTableWidget::item:selected {\n"
"    background-color: palette(highlight);\n"
"    color: palette(highlighted-text);\n"
"}\n"
"\n"
"/* \u89d2\u90e8\u6309\u94ae */\n"
"QTableCornerButton::section {\n"
"    background-color: palette(button);\n"
"    border: 1px solid palette(mid);\n"
"    border-top: none;\n"
"    border-left: none;\n"
"}\n"
"")
        self.ToSendingData.verticalHeader().setVisible(False)

        self.verticalLayout_16.addWidget(self.ToSendingData)


        self.verticalLayout_22.addWidget(self.verticalFrame_23)

        self.sendingPage.addWidget(self.page_2)

        self.verticalLayout_17.addWidget(self.sendingPage)


        self.verticalLayout_31.addWidget(self.verticalFrame_3)


        self.verticalLayout_33.addWidget(self.verticalFrame_2)

        self.verticalFrame_21 = QFrame(self.DownloadCheck)
        self.verticalFrame_21.setObjectName(u"verticalFrame_21")
        self.verticalFrame_21.setMinimumSize(QSize(0, 0))
        self.verticalLayout_35 = QVBoxLayout(self.verticalFrame_21)
        self.verticalLayout_35.setObjectName(u"verticalLayout_35")
        self.horizontalFrame_4 = QFrame(self.verticalFrame_21)
        self.horizontalFrame_4.setObjectName(u"horizontalFrame_4")
        self.horizontalFrame_4.setMinimumSize(QSize(0, 28))
        self.horizontalLayout_9 = QHBoxLayout(self.horizontalFrame_4)
        self.horizontalLayout_9.setObjectName(u"horizontalLayout_9")
        self.pushButton = QPushButton(self.horizontalFrame_4)
        self.pushButton.setObjectName(u"pushButton")
        self.pushButton.setStyleSheet(u"QPushButton {\n"
"    background-color: white;\n"
"    border: 1px solid #cccccc;\n"
"    border-bottom: none;\n"
"    font-weight: bold;\n"
"    padding: 0.4em 1.2em;  /* \u76f8\u5bf9\u5355\u4f4d */\n"
"    color: #333333;\n"
"    border-top-left-radius: 0.3em;\n"
"    border-top-right-radius: 0.3em;\n"
"}")

        self.horizontalLayout_9.addWidget(self.pushButton)

        self.label_2 = QLabel(self.horizontalFrame_4)
        self.label_2.setObjectName(u"label_2")

        self.horizontalLayout_9.addWidget(self.label_2)

        self.horizontalLayout_9.setStretch(0, 1)
        self.horizontalLayout_9.setStretch(1, 9)

        self.verticalLayout_35.addWidget(self.horizontalFrame_4)

        self.tableWidget_5 = HoverableTable(self.verticalFrame_21)
        if (self.tableWidget_5.columnCount() < 3):
            self.tableWidget_5.setColumnCount(3)
        __qtablewidgetitem220 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(0, __qtablewidgetitem220)
        __qtablewidgetitem221 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(1, __qtablewidgetitem221)
        __qtablewidgetitem222 = QTableWidgetItem()
        self.tableWidget_5.setHorizontalHeaderItem(2, __qtablewidgetitem222)
        if (self.tableWidget_5.rowCount() < 19):
            self.tableWidget_5.setRowCount(19)
        __qtablewidgetitem223 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(0, __qtablewidgetitem223)
        __qtablewidgetitem224 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(1, __qtablewidgetitem224)
        __qtablewidgetitem225 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(2, __qtablewidgetitem225)
        __qtablewidgetitem226 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(3, __qtablewidgetitem226)
        __qtablewidgetitem227 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(4, __qtablewidgetitem227)
        __qtablewidgetitem228 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(5, __qtablewidgetitem228)
        __qtablewidgetitem229 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(6, __qtablewidgetitem229)
        __qtablewidgetitem230 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(7, __qtablewidgetitem230)
        __qtablewidgetitem231 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(8, __qtablewidgetitem231)
        __qtablewidgetitem232 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(9, __qtablewidgetitem232)
        __qtablewidgetitem233 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(10, __qtablewidgetitem233)
        __qtablewidgetitem234 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(11, __qtablewidgetitem234)
        __qtablewidgetitem235 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(12, __qtablewidgetitem235)
        __qtablewidgetitem236 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(13, __qtablewidgetitem236)
        __qtablewidgetitem237 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(14, __qtablewidgetitem237)
        __qtablewidgetitem238 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(15, __qtablewidgetitem238)
        __qtablewidgetitem239 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(16, __qtablewidgetitem239)
        __qtablewidgetitem240 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(17, __qtablewidgetitem240)
        __qtablewidgetitem241 = QTableWidgetItem()
        self.tableWidget_5.setVerticalHeaderItem(18, __qtablewidgetitem241)
        __qtablewidgetitem242 = QTableWidgetItem()
        self.tableWidget_5.setItem(0, 0, __qtablewidgetitem242)
        __qtablewidgetitem243 = QTableWidgetItem()
        self.tableWidget_5.setItem(0, 1, __qtablewidgetitem243)
        __qtablewidgetitem244 = QTableWidgetItem()
        self.tableWidget_5.setItem(0, 2, __qtablewidgetitem244)
        __qtablewidgetitem245 = QTableWidgetItem()
        self.tableWidget_5.setItem(1, 0, __qtablewidgetitem245)
        __qtablewidgetitem246 = QTableWidgetItem()
        self.tableWidget_5.setItem(1, 1, __qtablewidgetitem246)
        __qtablewidgetitem247 = QTableWidgetItem()
        self.tableWidget_5.setItem(1, 2, __qtablewidgetitem247)
        __qtablewidgetitem248 = QTableWidgetItem()
        self.tableWidget_5.setItem(2, 0, __qtablewidgetitem248)
        __qtablewidgetitem249 = QTableWidgetItem()
        self.tableWidget_5.setItem(2, 1, __qtablewidgetitem249)
        __qtablewidgetitem250 = QTableWidgetItem()
        self.tableWidget_5.setItem(3, 0, __qtablewidgetitem250)
        __qtablewidgetitem251 = QTableWidgetItem()
        self.tableWidget_5.setItem(3, 1, __qtablewidgetitem251)
        __qtablewidgetitem252 = QTableWidgetItem()
        self.tableWidget_5.setItem(4, 0, __qtablewidgetitem252)
        __qtablewidgetitem253 = QTableWidgetItem()
        self.tableWidget_5.setItem(4, 1, __qtablewidgetitem253)
        __qtablewidgetitem254 = QTableWidgetItem()
        self.tableWidget_5.setItem(5, 0, __qtablewidgetitem254)
        __qtablewidgetitem255 = QTableWidgetItem()
        self.tableWidget_5.setItem(5, 1, __qtablewidgetitem255)
        self.tableWidget_5.setObjectName(u"tableWidget_5")
        self.tableWidget_5.setStyleSheet(u"/* \u4f7f\u7528\u7cfb\u7edf\u989c\u8272\u548c\u76f8\u5bf9\u5355\u4f4d */\n"
"QTableWidget {\n"
"    background-color: palette(base);\n"
"    gridline-color: palette(mid);\n"
"    border: 1px solid palette(mid);\n"
"    alternate-background-color: palette(alternate-base);\n"
"    font: inherit; /* \u7ee7\u627f\u7cfb\u7edf\u5b57\u4f53\u8bbe\u7f6e */\n"
"	gridline-color: transparent;\n"
"	show-decoration-selected: 1;\n"
"}\n"
"\n"
"/* \u8868\u5934\u6837\u5f0f - \u4f7f\u7528\u7cfb\u7edf\u8c03\u8272\u677f */\n"
"QHeaderView::section {\n"
"    background-color: palette(button);\n"
"    border-left: none;\n"
"    padding: 0.2em; /* \u4f7f\u7528\u76f8\u5bf9\u5355\u4f4d em */\n"
"    font-weight: bold;\n"
"    color: palette(text);\n"
"    min-height: 1.5em; /* \u76f8\u5bf9\u9ad8\u5ea6 */\n"
"	border: none; /* \u8868\u5934\u65e0\u8fb9\u6846 */\n"
"}\n"
"\n"
"/* \u8868\u683c\u5185\u5bb9\u9879\u6837\u5f0f */\n"
"QTableWidget::item {\n"
"    padding: 0.1em 0.3em; /* \u4e0a\u4e0b/\u5de6\u53f3\u5185\u8fb9\u8ddd */\n"
"}\n"
""
                        "\n"
"/* \u9009\u4e2d\u9879\u6837\u5f0f */\n"
"QTableWidget::item:selected {\n"
"    background-color: palette(highlight);\n"
"    color: palette(highlighted-text);\n"
"}\n"
"\n"
"/* \u89d2\u90e8\u6309\u94ae */\n"
"QTableCornerButton::section {\n"
"    background-color: palette(button);\n"
"    border: 1px solid palette(mid);\n"
"    border-top: none;\n"
"    border-left: none;\n"
"}\n"
"")
        self.tableWidget_5.verticalHeader().setVisible(False)

        self.verticalLayout_35.addWidget(self.tableWidget_5)


        self.verticalLayout_33.addWidget(self.verticalFrame_21)

        self.stackedWidget.addWidget(self.DownloadCheck)

        self.verticalLayout_15.addWidget(self.stackedWidget)


        self.horizontalLayout_4.addWidget(self.pagesContainer)

        self.extraRightBox = QFrame(self.content)
        self.extraRightBox.setObjectName(u"extraRightBox")
        self.extraRightBox.setMinimumSize(QSize(0, 0))
        self.extraRightBox.setMaximumSize(QSize(0, 16777215))
        self.extraRightBox.setFrameShape(QFrame.Shape.NoFrame)
        self.extraRightBox.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_7 = QVBoxLayout(self.extraRightBox)
        self.verticalLayout_7.setSpacing(0)
        self.verticalLayout_7.setObjectName(u"verticalLayout_7")
        self.verticalLayout_7.setContentsMargins(0, 0, 0, 0)
        self.themeSettingsTopDetail = QFrame(self.extraRightBox)
        self.themeSettingsTopDetail.setObjectName(u"themeSettingsTopDetail")
        self.themeSettingsTopDetail.setMaximumSize(QSize(16777215, 3))
        self.themeSettingsTopDetail.setFrameShape(QFrame.Shape.NoFrame)
        self.themeSettingsTopDetail.setFrameShadow(QFrame.Shadow.Raised)

        self.verticalLayout_7.addWidget(self.themeSettingsTopDetail)

        self.contentSettings = QFrame(self.extraRightBox)
        self.contentSettings.setObjectName(u"contentSettings")
        self.contentSettings.setFrameShape(QFrame.Shape.NoFrame)
        self.contentSettings.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_13 = QVBoxLayout(self.contentSettings)
        self.verticalLayout_13.setSpacing(0)
        self.verticalLayout_13.setObjectName(u"verticalLayout_13")
        self.verticalLayout_13.setContentsMargins(0, 0, 0, 0)
        self.topMenus = QFrame(self.contentSettings)
        self.topMenus.setObjectName(u"topMenus")
        self.topMenus.setFrameShape(QFrame.Shape.NoFrame)
        self.topMenus.setFrameShadow(QFrame.Shadow.Raised)
        self.verticalLayout_14 = QVBoxLayout(self.topMenus)
        self.verticalLayout_14.setSpacing(0)
        self.verticalLayout_14.setObjectName(u"verticalLayout_14")
        self.verticalLayout_14.setContentsMargins(0, 0, 0, 0)
        self.btn_message = QPushButton(self.topMenus)
        self.btn_message.setObjectName(u"btn_message")
        sizePolicy.setHeightForWidth(self.btn_message.sizePolicy().hasHeightForWidth())
        self.btn_message.setSizePolicy(sizePolicy)
        self.btn_message.setMinimumSize(QSize(0, 45))
        self.btn_message.setFont(font)
        self.btn_message.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_message.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_message.setStyleSheet(u"background-image: url(:/icons/icons/cil-envelope-open.png);")

        self.verticalLayout_14.addWidget(self.btn_message)

        self.btn_print = QPushButton(self.topMenus)
        self.btn_print.setObjectName(u"btn_print")
        sizePolicy.setHeightForWidth(self.btn_print.sizePolicy().hasHeightForWidth())
        self.btn_print.setSizePolicy(sizePolicy)
        self.btn_print.setMinimumSize(QSize(0, 45))
        self.btn_print.setFont(font)
        self.btn_print.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_print.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_print.setStyleSheet(u"background-image: url(:/icons/icons/cil-print.png);")

        self.verticalLayout_14.addWidget(self.btn_print)

        self.btn_logout = QPushButton(self.topMenus)
        self.btn_logout.setObjectName(u"btn_logout")
        sizePolicy.setHeightForWidth(self.btn_logout.sizePolicy().hasHeightForWidth())
        self.btn_logout.setSizePolicy(sizePolicy)
        self.btn_logout.setMinimumSize(QSize(0, 45))
        self.btn_logout.setFont(font)
        self.btn_logout.setCursor(QCursor(Qt.CursorShape.PointingHandCursor))
        self.btn_logout.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        self.btn_logout.setStyleSheet(u"background-image: url(:/icons/icons/cil-account-logout.png);")

        self.verticalLayout_14.addWidget(self.btn_logout)


        self.verticalLayout_13.addWidget(self.topMenus, 0, Qt.AlignmentFlag.AlignTop)


        self.verticalLayout_7.addWidget(self.contentSettings)


        self.horizontalLayout_4.addWidget(self.extraRightBox)


        self.verticalLayout_6.addWidget(self.content)

        self.bottomBar = QFrame(self.contentBottom)
        self.bottomBar.setObjectName(u"bottomBar")
        self.bottomBar.setMinimumSize(QSize(0, 22))
        self.bottomBar.setMaximumSize(QSize(16777215, 22))
        self.bottomBar.setFrameShape(QFrame.Shape.NoFrame)
        self.bottomBar.setFrameShadow(QFrame.Shadow.Raised)
        self.horizontalLayout_5 = QHBoxLayout(self.bottomBar)
        self.horizontalLayout_5.setSpacing(0)
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.creditsLabel = QLabel(self.bottomBar)
        self.creditsLabel.setObjectName(u"creditsLabel")
        self.creditsLabel.setMaximumSize(QSize(16777215, 16))
        font2 = QFont()
        font2.setFamilies([u"Segoe UI"])
        font2.setBold(False)
        font2.setItalic(False)
        self.creditsLabel.setFont(font2)
        self.creditsLabel.setAlignment(Qt.AlignmentFlag.AlignLeading|Qt.AlignmentFlag.AlignLeft|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.creditsLabel)

        self.version = QLabel(self.bottomBar)
        self.version.setObjectName(u"version")
        self.version.setAlignment(Qt.AlignmentFlag.AlignRight|Qt.AlignmentFlag.AlignTrailing|Qt.AlignmentFlag.AlignVCenter)

        self.horizontalLayout_5.addWidget(self.version)

        self.frame_size_grip = QFrame(self.bottomBar)
        self.frame_size_grip.setObjectName(u"frame_size_grip")
        self.frame_size_grip.setMinimumSize(QSize(20, 0))
        self.frame_size_grip.setMaximumSize(QSize(20, 16777215))
        self.frame_size_grip.setFrameShape(QFrame.Shape.NoFrame)
        self.frame_size_grip.setFrameShadow(QFrame.Shadow.Raised)

        self.horizontalLayout_5.addWidget(self.frame_size_grip)


        self.verticalLayout_6.addWidget(self.bottomBar)


        self.verticalLayout_2.addWidget(self.contentBottom)


        self.appLayout.addWidget(self.contentBox)


        self.horizontalLayout_7.addWidget(self.bgApp)

        MainWindow.setCentralWidget(self.styleSheet)

        self.retranslateUi(MainWindow)

        self.stackedWidget.setCurrentIndex(2)
        self.sendingPage.setCurrentIndex(1)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.toggleButton.setText(QCoreApplication.translate("MainWindow", u"Hide", None))
        self.btn_home.setText(QCoreApplication.translate("MainWindow", u"Home", None))
        self.btn_widgets.setText(QCoreApplication.translate("MainWindow", u"Widgets", None))
        self.btn_new.setText(QCoreApplication.translate("MainWindow", u"New", None))
        self.extraLabel.setText(QCoreApplication.translate("MainWindow", u"Searching Devices", None))
        self.pushButton_4.setText("")
#if QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close left box", None))
#endif // QT_CONFIG(tooltip)
        self.extraCloseColumnBtn.setText("")
        self.btn_adjustments.setText(QCoreApplication.translate("MainWindow", u"Click For Searching", None))
        ___qtablewidgetitem = self.peer.horizontalHeaderItem(0)
        ___qtablewidgetitem.setText(QCoreApplication.translate("MainWindow", u"devices", None));
        ___qtablewidgetitem1 = self.peer.verticalHeaderItem(0)
        ___qtablewidgetitem1.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem2 = self.peer.verticalHeaderItem(1)
        ___qtablewidgetitem2.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem3 = self.peer.verticalHeaderItem(2)
        ___qtablewidgetitem3.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem4 = self.peer.verticalHeaderItem(3)
        ___qtablewidgetitem4.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem5 = self.peer.verticalHeaderItem(4)
        ___qtablewidgetitem5.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem6 = self.peer.verticalHeaderItem(5)
        ___qtablewidgetitem6.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem7 = self.peer.verticalHeaderItem(6)
        ___qtablewidgetitem7.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem8 = self.peer.verticalHeaderItem(7)
        ___qtablewidgetitem8.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem9 = self.peer.verticalHeaderItem(8)
        ___qtablewidgetitem9.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem10 = self.peer.verticalHeaderItem(9)
        ___qtablewidgetitem10.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem11 = self.peer.verticalHeaderItem(10)
        ___qtablewidgetitem11.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem12 = self.peer.verticalHeaderItem(11)
        ___qtablewidgetitem12.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem13 = self.peer.verticalHeaderItem(12)
        ___qtablewidgetitem13.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));

        __sortingEnabled = self.peer.isSortingEnabled()
        self.peer.setSortingEnabled(False)
        ___qtablewidgetitem14 = self.peer.item(0, 0)
        ___qtablewidgetitem14.setText(QCoreApplication.translate("MainWindow", u"128.0.0.1:8080", None));
        ___qtablewidgetitem15 = self.peer.item(1, 0)
        ___qtablewidgetitem15.setText(QCoreApplication.translate("MainWindow", u"128.0.0.1:8080", None));
        ___qtablewidgetitem16 = self.peer.item(2, 0)
        ___qtablewidgetitem16.setText(QCoreApplication.translate("MainWindow", u"128.0.0.1:8080", None));
        ___qtablewidgetitem17 = self.peer.item(3, 0)
        ___qtablewidgetitem17.setText(QCoreApplication.translate("MainWindow", u"128.0.0.1:8080", None));
        ___qtablewidgetitem18 = self.peer.item(4, 0)
        ___qtablewidgetitem18.setText(QCoreApplication.translate("MainWindow", u"128.0.0.1:8080", None));
        ___qtablewidgetitem19 = self.peer.item(5, 0)
        ___qtablewidgetitem19.setText(QCoreApplication.translate("MainWindow", u"128.0.0.1:8080", None));
        ___qtablewidgetitem20 = self.peer.item(6, 0)
        ___qtablewidgetitem20.setText(QCoreApplication.translate("MainWindow", u"128.0.0.1:8080", None));
        ___qtablewidgetitem21 = self.peer.item(7, 0)
        ___qtablewidgetitem21.setText(QCoreApplication.translate("MainWindow", u"128.0.0.1:8080", None));
        ___qtablewidgetitem22 = self.peer.item(8, 0)
        ___qtablewidgetitem22.setText(QCoreApplication.translate("MainWindow", u"128.0.0.1:8080", None));
        ___qtablewidgetitem23 = self.peer.item(9, 0)
        ___qtablewidgetitem23.setText(QCoreApplication.translate("MainWindow", u"128.0.0.1:8080", None));
        ___qtablewidgetitem24 = self.peer.item(10, 0)
        ___qtablewidgetitem24.setText(QCoreApplication.translate("MainWindow", u"128.0.0.1:8080", None));
        ___qtablewidgetitem25 = self.peer.item(11, 0)
        ___qtablewidgetitem25.setText(QCoreApplication.translate("MainWindow", u"128.0.0.1:8080", None));
        ___qtablewidgetitem26 = self.peer.item(12, 0)
        ___qtablewidgetitem26.setText(QCoreApplication.translate("MainWindow", u"128.0.0.1:8080", None));
        self.peer.setSortingEnabled(__sortingEnabled)

        self.titleRightInfo.setText(QCoreApplication.translate("MainWindow", u"MN Local File Sharing System", None))
#if QT_CONFIG(tooltip)
        self.minimizeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Minimize", None))
#endif // QT_CONFIG(tooltip)
        self.minimizeAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Maximize", None))
#endif // QT_CONFIG(tooltip)
        self.maximizeRestoreAppBtn.setText("")
#if QT_CONFIG(tooltip)
        self.closeAppBtn.setToolTip(QCoreApplication.translate("MainWindow", u"Close", None))
#endif // QT_CONFIG(tooltip)
        self.closeAppBtn.setText("")
        self.pushButton_2.setText(QCoreApplication.translate("MainWindow", u"C:Program Files (x86)Common Files", None))
        ___qtablewidgetitem27 = self.tableWidget_2.horizontalHeaderItem(0)
        ___qtablewidgetitem27.setText(QCoreApplication.translate("MainWindow", u"\u540d\u5b57", None));
        ___qtablewidgetitem28 = self.tableWidget_2.horizontalHeaderItem(1)
        ___qtablewidgetitem28.setText(QCoreApplication.translate("MainWindow", u"\u5927\u5c0f", None));
        ___qtablewidgetitem29 = self.tableWidget_2.horizontalHeaderItem(2)
        ___qtablewidgetitem29.setText(QCoreApplication.translate("MainWindow", u"\u7c7b\u578b", None));
        ___qtablewidgetitem30 = self.tableWidget_2.verticalHeaderItem(0)
        ___qtablewidgetitem30.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem31 = self.tableWidget_2.verticalHeaderItem(1)
        ___qtablewidgetitem31.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem32 = self.tableWidget_2.verticalHeaderItem(2)
        ___qtablewidgetitem32.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem33 = self.tableWidget_2.verticalHeaderItem(3)
        ___qtablewidgetitem33.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem34 = self.tableWidget_2.verticalHeaderItem(4)
        ___qtablewidgetitem34.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem35 = self.tableWidget_2.verticalHeaderItem(5)
        ___qtablewidgetitem35.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem36 = self.tableWidget_2.verticalHeaderItem(6)
        ___qtablewidgetitem36.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem37 = self.tableWidget_2.verticalHeaderItem(7)
        ___qtablewidgetitem37.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem38 = self.tableWidget_2.verticalHeaderItem(8)
        ___qtablewidgetitem38.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem39 = self.tableWidget_2.verticalHeaderItem(9)
        ___qtablewidgetitem39.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem40 = self.tableWidget_2.verticalHeaderItem(10)
        ___qtablewidgetitem40.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem41 = self.tableWidget_2.verticalHeaderItem(11)
        ___qtablewidgetitem41.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem42 = self.tableWidget_2.verticalHeaderItem(12)
        ___qtablewidgetitem42.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem43 = self.tableWidget_2.verticalHeaderItem(13)
        ___qtablewidgetitem43.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem44 = self.tableWidget_2.verticalHeaderItem(14)
        ___qtablewidgetitem44.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem45 = self.tableWidget_2.verticalHeaderItem(15)
        ___qtablewidgetitem45.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem46 = self.tableWidget_2.verticalHeaderItem(16)
        ___qtablewidgetitem46.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem47 = self.tableWidget_2.verticalHeaderItem(17)
        ___qtablewidgetitem47.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem48 = self.tableWidget_2.verticalHeaderItem(18)
        ___qtablewidgetitem48.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem49 = self.tableWidget_2.verticalHeaderItem(19)
        ___qtablewidgetitem49.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));

        __sortingEnabled1 = self.tableWidget_2.isSortingEnabled()
        self.tableWidget_2.setSortingEnabled(False)
        ___qtablewidgetitem50 = self.tableWidget_2.item(0, 0)
        ___qtablewidgetitem50.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem51 = self.tableWidget_2.item(0, 1)
        ___qtablewidgetitem51.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem52 = self.tableWidget_2.item(0, 2)
        ___qtablewidgetitem52.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem53 = self.tableWidget_2.item(1, 0)
        ___qtablewidgetitem53.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem54 = self.tableWidget_2.item(1, 1)
        ___qtablewidgetitem54.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem55 = self.tableWidget_2.item(1, 2)
        ___qtablewidgetitem55.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem56 = self.tableWidget_2.item(2, 0)
        ___qtablewidgetitem56.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem57 = self.tableWidget_2.item(2, 1)
        ___qtablewidgetitem57.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem58 = self.tableWidget_2.item(2, 2)
        ___qtablewidgetitem58.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem59 = self.tableWidget_2.item(3, 0)
        ___qtablewidgetitem59.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem60 = self.tableWidget_2.item(3, 1)
        ___qtablewidgetitem60.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem61 = self.tableWidget_2.item(3, 2)
        ___qtablewidgetitem61.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem62 = self.tableWidget_2.item(4, 0)
        ___qtablewidgetitem62.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem63 = self.tableWidget_2.item(4, 1)
        ___qtablewidgetitem63.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem64 = self.tableWidget_2.item(4, 2)
        ___qtablewidgetitem64.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem65 = self.tableWidget_2.item(5, 0)
        ___qtablewidgetitem65.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem66 = self.tableWidget_2.item(5, 1)
        ___qtablewidgetitem66.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem67 = self.tableWidget_2.item(5, 2)
        ___qtablewidgetitem67.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem68 = self.tableWidget_2.item(6, 0)
        ___qtablewidgetitem68.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem69 = self.tableWidget_2.item(6, 1)
        ___qtablewidgetitem69.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem70 = self.tableWidget_2.item(6, 2)
        ___qtablewidgetitem70.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem71 = self.tableWidget_2.item(13, 0)
        ___qtablewidgetitem71.setText(QCoreApplication.translate("MainWindow", u"\u5927\u5c0f", None));
        ___qtablewidgetitem72 = self.tableWidget_2.item(13, 2)
        ___qtablewidgetitem72.setText(QCoreApplication.translate("MainWindow", u"\u7c7b\u578b", None));
        ___qtablewidgetitem73 = self.tableWidget_2.item(14, 0)
        ___qtablewidgetitem73.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem74 = self.tableWidget_2.item(14, 2)
        ___qtablewidgetitem74.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem75 = self.tableWidget_2.item(15, 0)
        ___qtablewidgetitem75.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem76 = self.tableWidget_2.item(15, 2)
        ___qtablewidgetitem76.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem77 = self.tableWidget_2.item(17, 0)
        ___qtablewidgetitem77.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem78 = self.tableWidget_2.item(17, 2)
        ___qtablewidgetitem78.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem79 = self.tableWidget_2.item(18, 0)
        ___qtablewidgetitem79.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        self.tableWidget_2.setSortingEnabled(__sortingEnabled1)

        self.FileSharingLabel.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        ___qtablewidgetitem80 = self.tableWidget_3.horizontalHeaderItem(0)
        ___qtablewidgetitem80.setText(QCoreApplication.translate("MainWindow", u"\u540d\u5b57", None));
        ___qtablewidgetitem81 = self.tableWidget_3.horizontalHeaderItem(1)
        ___qtablewidgetitem81.setText(QCoreApplication.translate("MainWindow", u"\u5927\u5c0f", None));
        ___qtablewidgetitem82 = self.tableWidget_3.horizontalHeaderItem(2)
        ___qtablewidgetitem82.setText(QCoreApplication.translate("MainWindow", u"\u7c7b\u578b", None));
        ___qtablewidgetitem83 = self.tableWidget_3.verticalHeaderItem(0)
        ___qtablewidgetitem83.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem84 = self.tableWidget_3.verticalHeaderItem(1)
        ___qtablewidgetitem84.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem85 = self.tableWidget_3.verticalHeaderItem(2)
        ___qtablewidgetitem85.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem86 = self.tableWidget_3.verticalHeaderItem(3)
        ___qtablewidgetitem86.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem87 = self.tableWidget_3.verticalHeaderItem(4)
        ___qtablewidgetitem87.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem88 = self.tableWidget_3.verticalHeaderItem(5)
        ___qtablewidgetitem88.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem89 = self.tableWidget_3.verticalHeaderItem(6)
        ___qtablewidgetitem89.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem90 = self.tableWidget_3.verticalHeaderItem(7)
        ___qtablewidgetitem90.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem91 = self.tableWidget_3.verticalHeaderItem(8)
        ___qtablewidgetitem91.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem92 = self.tableWidget_3.verticalHeaderItem(9)
        ___qtablewidgetitem92.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem93 = self.tableWidget_3.verticalHeaderItem(10)
        ___qtablewidgetitem93.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem94 = self.tableWidget_3.verticalHeaderItem(11)
        ___qtablewidgetitem94.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem95 = self.tableWidget_3.verticalHeaderItem(12)
        ___qtablewidgetitem95.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem96 = self.tableWidget_3.verticalHeaderItem(13)
        ___qtablewidgetitem96.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem97 = self.tableWidget_3.verticalHeaderItem(14)
        ___qtablewidgetitem97.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem98 = self.tableWidget_3.verticalHeaderItem(15)
        ___qtablewidgetitem98.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem99 = self.tableWidget_3.verticalHeaderItem(16)
        ___qtablewidgetitem99.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem100 = self.tableWidget_3.verticalHeaderItem(17)
        ___qtablewidgetitem100.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem101 = self.tableWidget_3.verticalHeaderItem(18)
        ___qtablewidgetitem101.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem102 = self.tableWidget_3.verticalHeaderItem(19)
        ___qtablewidgetitem102.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem103 = self.tableWidget_3.verticalHeaderItem(20)
        ___qtablewidgetitem103.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));

        __sortingEnabled2 = self.tableWidget_3.isSortingEnabled()
        self.tableWidget_3.setSortingEnabled(False)
        ___qtablewidgetitem104 = self.tableWidget_3.item(0, 0)
        ___qtablewidgetitem104.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem105 = self.tableWidget_3.item(0, 1)
        ___qtablewidgetitem105.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem106 = self.tableWidget_3.item(0, 2)
        ___qtablewidgetitem106.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem107 = self.tableWidget_3.item(1, 0)
        ___qtablewidgetitem107.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem108 = self.tableWidget_3.item(1, 1)
        ___qtablewidgetitem108.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem109 = self.tableWidget_3.item(1, 2)
        ___qtablewidgetitem109.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem110 = self.tableWidget_3.item(2, 0)
        ___qtablewidgetitem110.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem111 = self.tableWidget_3.item(2, 1)
        ___qtablewidgetitem111.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem112 = self.tableWidget_3.item(2, 2)
        ___qtablewidgetitem112.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem113 = self.tableWidget_3.item(3, 0)
        ___qtablewidgetitem113.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem114 = self.tableWidget_3.item(3, 1)
        ___qtablewidgetitem114.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem115 = self.tableWidget_3.item(3, 2)
        ___qtablewidgetitem115.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem116 = self.tableWidget_3.item(4, 0)
        ___qtablewidgetitem116.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem117 = self.tableWidget_3.item(4, 1)
        ___qtablewidgetitem117.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem118 = self.tableWidget_3.item(4, 2)
        ___qtablewidgetitem118.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem119 = self.tableWidget_3.item(5, 0)
        ___qtablewidgetitem119.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem120 = self.tableWidget_3.item(5, 1)
        ___qtablewidgetitem120.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem121 = self.tableWidget_3.item(5, 2)
        ___qtablewidgetitem121.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem122 = self.tableWidget_3.item(6, 0)
        ___qtablewidgetitem122.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem123 = self.tableWidget_3.item(6, 1)
        ___qtablewidgetitem123.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem124 = self.tableWidget_3.item(6, 2)
        ___qtablewidgetitem124.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem125 = self.tableWidget_3.item(7, 0)
        ___qtablewidgetitem125.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem126 = self.tableWidget_3.item(8, 0)
        ___qtablewidgetitem126.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem127 = self.tableWidget_3.item(9, 0)
        ___qtablewidgetitem127.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem128 = self.tableWidget_3.item(9, 2)
        ___qtablewidgetitem128.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem129 = self.tableWidget_3.item(10, 0)
        ___qtablewidgetitem129.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem130 = self.tableWidget_3.item(11, 1)
        ___qtablewidgetitem130.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem131 = self.tableWidget_3.item(12, 0)
        ___qtablewidgetitem131.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem132 = self.tableWidget_3.item(13, 1)
        ___qtablewidgetitem132.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem133 = self.tableWidget_3.item(13, 2)
        ___qtablewidgetitem133.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        self.tableWidget_3.setSortingEnabled(__sortingEnabled2)

        self.HostLabel.setText(QCoreApplication.translate("MainWindow", u"Host: 127.0.0.1:8080", None))
        self.pushButton_3.setText(QCoreApplication.translate("MainWindow", u"C:\\Program Files (x86)\\Common Files\\LenovoAppStoreNotify", None))
        ___qtablewidgetitem134 = self.PeerLabel.horizontalHeaderItem(0)
        ___qtablewidgetitem134.setText(QCoreApplication.translate("MainWindow", u"\u540d\u5b57", None));
        ___qtablewidgetitem135 = self.PeerLabel.horizontalHeaderItem(1)
        ___qtablewidgetitem135.setText(QCoreApplication.translate("MainWindow", u"\u5927\u5c0f", None));
        ___qtablewidgetitem136 = self.PeerLabel.horizontalHeaderItem(2)
        ___qtablewidgetitem136.setText(QCoreApplication.translate("MainWindow", u"\u7c7b\u578b", None));
        ___qtablewidgetitem137 = self.PeerLabel.verticalHeaderItem(0)
        ___qtablewidgetitem137.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem138 = self.PeerLabel.verticalHeaderItem(1)
        ___qtablewidgetitem138.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem139 = self.PeerLabel.verticalHeaderItem(2)
        ___qtablewidgetitem139.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem140 = self.PeerLabel.verticalHeaderItem(3)
        ___qtablewidgetitem140.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem141 = self.PeerLabel.verticalHeaderItem(4)
        ___qtablewidgetitem141.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem142 = self.PeerLabel.verticalHeaderItem(5)
        ___qtablewidgetitem142.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem143 = self.PeerLabel.verticalHeaderItem(6)
        ___qtablewidgetitem143.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem144 = self.PeerLabel.verticalHeaderItem(7)
        ___qtablewidgetitem144.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem145 = self.PeerLabel.verticalHeaderItem(8)
        ___qtablewidgetitem145.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem146 = self.PeerLabel.verticalHeaderItem(9)
        ___qtablewidgetitem146.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem147 = self.PeerLabel.verticalHeaderItem(10)
        ___qtablewidgetitem147.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem148 = self.PeerLabel.verticalHeaderItem(11)
        ___qtablewidgetitem148.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem149 = self.PeerLabel.verticalHeaderItem(12)
        ___qtablewidgetitem149.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem150 = self.PeerLabel.verticalHeaderItem(13)
        ___qtablewidgetitem150.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem151 = self.PeerLabel.verticalHeaderItem(14)
        ___qtablewidgetitem151.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem152 = self.PeerLabel.verticalHeaderItem(15)
        ___qtablewidgetitem152.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem153 = self.PeerLabel.verticalHeaderItem(16)
        ___qtablewidgetitem153.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem154 = self.PeerLabel.verticalHeaderItem(17)
        ___qtablewidgetitem154.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem155 = self.PeerLabel.verticalHeaderItem(18)
        ___qtablewidgetitem155.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem156 = self.PeerLabel.verticalHeaderItem(19)
        ___qtablewidgetitem156.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem157 = self.PeerLabel.verticalHeaderItem(20)
        ___qtablewidgetitem157.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));

        __sortingEnabled3 = self.PeerLabel.isSortingEnabled()
        self.PeerLabel.setSortingEnabled(False)
        ___qtablewidgetitem158 = self.PeerLabel.item(0, 0)
        ___qtablewidgetitem158.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem159 = self.PeerLabel.item(0, 1)
        ___qtablewidgetitem159.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem160 = self.PeerLabel.item(0, 2)
        ___qtablewidgetitem160.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem161 = self.PeerLabel.item(1, 0)
        ___qtablewidgetitem161.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem162 = self.PeerLabel.item(1, 1)
        ___qtablewidgetitem162.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem163 = self.PeerLabel.item(2, 2)
        ___qtablewidgetitem163.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem164 = self.PeerLabel.item(3, 0)
        ___qtablewidgetitem164.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem165 = self.PeerLabel.item(3, 1)
        ___qtablewidgetitem165.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem166 = self.PeerLabel.item(4, 0)
        ___qtablewidgetitem166.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem167 = self.PeerLabel.item(5, 1)
        ___qtablewidgetitem167.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem168 = self.PeerLabel.item(5, 2)
        ___qtablewidgetitem168.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem169 = self.PeerLabel.item(6, 0)
        ___qtablewidgetitem169.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem170 = self.PeerLabel.item(13, 0)
        ___qtablewidgetitem170.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem171 = self.PeerLabel.item(13, 1)
        ___qtablewidgetitem171.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem172 = self.PeerLabel.item(13, 2)
        ___qtablewidgetitem172.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem173 = self.PeerLabel.item(14, 0)
        ___qtablewidgetitem173.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem174 = self.PeerLabel.item(14, 1)
        ___qtablewidgetitem174.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem175 = self.PeerLabel.item(14, 2)
        ___qtablewidgetitem175.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem176 = self.PeerLabel.item(15, 0)
        ___qtablewidgetitem176.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem177 = self.PeerLabel.item(15, 1)
        ___qtablewidgetitem177.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem178 = self.PeerLabel.item(15, 2)
        ___qtablewidgetitem178.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem179 = self.PeerLabel.item(16, 0)
        ___qtablewidgetitem179.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem180 = self.PeerLabel.item(17, 0)
        ___qtablewidgetitem180.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem181 = self.PeerLabel.item(18, 1)
        ___qtablewidgetitem181.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem182 = self.PeerLabel.item(19, 0)
        ___qtablewidgetitem182.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem183 = self.PeerLabel.item(19, 1)
        ___qtablewidgetitem183.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem184 = self.PeerLabel.item(20, 0)
        ___qtablewidgetitem184.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem185 = self.PeerLabel.item(20, 1)
        ___qtablewidgetitem185.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        self.PeerLabel.setSortingEnabled(__sortingEnabled3)

        self.FromLocal.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.ToLocal.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label.setText("")
        ___qtablewidgetitem186 = self.FromSendingData.horizontalHeaderItem(0)
        ___qtablewidgetitem186.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None));
        ___qtablewidgetitem187 = self.FromSendingData.horizontalHeaderItem(1)
        ___qtablewidgetitem187.setText(QCoreApplication.translate("MainWindow", u"\u5927\u5c0f", None));
        ___qtablewidgetitem188 = self.FromSendingData.horizontalHeaderItem(2)
        ___qtablewidgetitem188.setText(QCoreApplication.translate("MainWindow", u"\u72b6\u6001", None));
        ___qtablewidgetitem189 = self.FromSendingData.verticalHeaderItem(0)
        ___qtablewidgetitem189.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem190 = self.FromSendingData.verticalHeaderItem(1)
        ___qtablewidgetitem190.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem191 = self.FromSendingData.verticalHeaderItem(2)
        ___qtablewidgetitem191.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem192 = self.FromSendingData.verticalHeaderItem(3)
        ___qtablewidgetitem192.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem193 = self.FromSendingData.verticalHeaderItem(4)
        ___qtablewidgetitem193.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem194 = self.FromSendingData.verticalHeaderItem(5)
        ___qtablewidgetitem194.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem195 = self.FromSendingData.verticalHeaderItem(6)
        ___qtablewidgetitem195.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));

        __sortingEnabled4 = self.FromSendingData.isSortingEnabled()
        self.FromSendingData.setSortingEnabled(False)
        ___qtablewidgetitem196 = self.FromSendingData.item(0, 0)
        ___qtablewidgetitem196.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem197 = self.FromSendingData.item(1, 2)
        ___qtablewidgetitem197.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem198 = self.FromSendingData.item(2, 1)
        ___qtablewidgetitem198.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem199 = self.FromSendingData.item(2, 2)
        ___qtablewidgetitem199.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem200 = self.FromSendingData.item(3, 0)
        ___qtablewidgetitem200.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem201 = self.FromSendingData.item(4, 2)
        ___qtablewidgetitem201.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem202 = self.FromSendingData.item(5, 1)
        ___qtablewidgetitem202.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem203 = self.FromSendingData.item(6, 1)
        ___qtablewidgetitem203.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        self.FromSendingData.setSortingEnabled(__sortingEnabled4)

        ___qtablewidgetitem204 = self.ToSendingData.horizontalHeaderItem(0)
        ___qtablewidgetitem204.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None));
        ___qtablewidgetitem205 = self.ToSendingData.horizontalHeaderItem(1)
        ___qtablewidgetitem205.setText(QCoreApplication.translate("MainWindow", u"\u5927\u5c0f", None));
        ___qtablewidgetitem206 = self.ToSendingData.horizontalHeaderItem(2)
        ___qtablewidgetitem206.setText(QCoreApplication.translate("MainWindow", u"\u72b6\u6001", None));
        ___qtablewidgetitem207 = self.ToSendingData.verticalHeaderItem(0)
        ___qtablewidgetitem207.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem208 = self.ToSendingData.verticalHeaderItem(1)
        ___qtablewidgetitem208.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem209 = self.ToSendingData.verticalHeaderItem(2)
        ___qtablewidgetitem209.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem210 = self.ToSendingData.verticalHeaderItem(3)
        ___qtablewidgetitem210.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem211 = self.ToSendingData.verticalHeaderItem(4)
        ___qtablewidgetitem211.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem212 = self.ToSendingData.verticalHeaderItem(5)
        ___qtablewidgetitem212.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));

        __sortingEnabled5 = self.ToSendingData.isSortingEnabled()
        self.ToSendingData.setSortingEnabled(False)
        ___qtablewidgetitem213 = self.ToSendingData.item(0, 0)
        ___qtablewidgetitem213.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem214 = self.ToSendingData.item(1, 0)
        ___qtablewidgetitem214.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem215 = self.ToSendingData.item(2, 1)
        ___qtablewidgetitem215.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem216 = self.ToSendingData.item(3, 1)
        ___qtablewidgetitem216.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem217 = self.ToSendingData.item(4, 1)
        ___qtablewidgetitem217.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem218 = self.ToSendingData.item(5, 1)
        ___qtablewidgetitem218.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem219 = self.ToSendingData.item(5, 2)
        ___qtablewidgetitem219.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        self.ToSendingData.setSortingEnabled(__sortingEnabled5)

        self.pushButton.setText(QCoreApplication.translate("MainWindow", u"PushButton", None))
        self.label_2.setText("")
        ___qtablewidgetitem220 = self.tableWidget_5.horizontalHeaderItem(0)
        ___qtablewidgetitem220.setText(QCoreApplication.translate("MainWindow", u"\u6587\u4ef6", None));
        ___qtablewidgetitem221 = self.tableWidget_5.horizontalHeaderItem(1)
        ___qtablewidgetitem221.setText(QCoreApplication.translate("MainWindow", u"\u5927\u5c0f", None));
        ___qtablewidgetitem222 = self.tableWidget_5.horizontalHeaderItem(2)
        ___qtablewidgetitem222.setText(QCoreApplication.translate("MainWindow", u"\u63a5\u6536\u4e2d", None));
        ___qtablewidgetitem223 = self.tableWidget_5.verticalHeaderItem(0)
        ___qtablewidgetitem223.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem224 = self.tableWidget_5.verticalHeaderItem(1)
        ___qtablewidgetitem224.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem225 = self.tableWidget_5.verticalHeaderItem(2)
        ___qtablewidgetitem225.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem226 = self.tableWidget_5.verticalHeaderItem(3)
        ___qtablewidgetitem226.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem227 = self.tableWidget_5.verticalHeaderItem(4)
        ___qtablewidgetitem227.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem228 = self.tableWidget_5.verticalHeaderItem(5)
        ___qtablewidgetitem228.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem229 = self.tableWidget_5.verticalHeaderItem(6)
        ___qtablewidgetitem229.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem230 = self.tableWidget_5.verticalHeaderItem(7)
        ___qtablewidgetitem230.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem231 = self.tableWidget_5.verticalHeaderItem(8)
        ___qtablewidgetitem231.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem232 = self.tableWidget_5.verticalHeaderItem(9)
        ___qtablewidgetitem232.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem233 = self.tableWidget_5.verticalHeaderItem(10)
        ___qtablewidgetitem233.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem234 = self.tableWidget_5.verticalHeaderItem(11)
        ___qtablewidgetitem234.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem235 = self.tableWidget_5.verticalHeaderItem(12)
        ___qtablewidgetitem235.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem236 = self.tableWidget_5.verticalHeaderItem(13)
        ___qtablewidgetitem236.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem237 = self.tableWidget_5.verticalHeaderItem(14)
        ___qtablewidgetitem237.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem238 = self.tableWidget_5.verticalHeaderItem(15)
        ___qtablewidgetitem238.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem239 = self.tableWidget_5.verticalHeaderItem(16)
        ___qtablewidgetitem239.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem240 = self.tableWidget_5.verticalHeaderItem(17)
        ___qtablewidgetitem240.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));
        ___qtablewidgetitem241 = self.tableWidget_5.verticalHeaderItem(18)
        ___qtablewidgetitem241.setText(QCoreApplication.translate("MainWindow", u"\u65b0\u5efa\u884c", None));

        __sortingEnabled6 = self.tableWidget_5.isSortingEnabled()
        self.tableWidget_5.setSortingEnabled(False)
        ___qtablewidgetitem242 = self.tableWidget_5.item(0, 0)
        ___qtablewidgetitem242.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem243 = self.tableWidget_5.item(0, 1)
        ___qtablewidgetitem243.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem244 = self.tableWidget_5.item(0, 2)
        ___qtablewidgetitem244.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem245 = self.tableWidget_5.item(1, 0)
        ___qtablewidgetitem245.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem246 = self.tableWidget_5.item(1, 1)
        ___qtablewidgetitem246.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem247 = self.tableWidget_5.item(1, 2)
        ___qtablewidgetitem247.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem248 = self.tableWidget_5.item(2, 0)
        ___qtablewidgetitem248.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem249 = self.tableWidget_5.item(2, 1)
        ___qtablewidgetitem249.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem250 = self.tableWidget_5.item(3, 0)
        ___qtablewidgetitem250.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem251 = self.tableWidget_5.item(3, 1)
        ___qtablewidgetitem251.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem252 = self.tableWidget_5.item(4, 0)
        ___qtablewidgetitem252.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem253 = self.tableWidget_5.item(4, 1)
        ___qtablewidgetitem253.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem254 = self.tableWidget_5.item(5, 0)
        ___qtablewidgetitem254.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        ___qtablewidgetitem255 = self.tableWidget_5.item(5, 1)
        ___qtablewidgetitem255.setText(QCoreApplication.translate("MainWindow", u"demo", None));
        self.tableWidget_5.setSortingEnabled(__sortingEnabled6)

        self.btn_message.setText(QCoreApplication.translate("MainWindow", u"Message", None))
        self.btn_print.setText(QCoreApplication.translate("MainWindow", u"Print", None))
        self.btn_logout.setText(QCoreApplication.translate("MainWindow", u"Logout", None))
        self.creditsLabel.setText("")
        self.version.setText(QCoreApplication.translate("MainWindow", u"v1.0.0", None))
    # retranslateUi

