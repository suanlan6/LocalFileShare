import sys
from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QTableWidget,
    QTableWidgetItem,
    QWidget,
    QHBoxLayout,
    QPushButton,
    QHeaderView,
)
from PySide6.QtGui import QIcon, QCursor
from PySide6.QtCore import Qt, QSize, QObject, QEvent, Signal

# from src.LFS_GUI.views.ui_designs.hover_table import HoverableTable


class ButtonSendingWidget(QWidget):
    rowDeleted = Signal(str, int)
    # 第二位标志，0为暂停了，1为继续了
    rowChanged = Signal(str, int, int)

    def __init__(self, row, status, parent=None):
        super().__init__(parent)
        self.row = row
        self.status = status
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        self.btn1 = QPushButton()

        self.close_icon = QIcon(":/icons/icons/play.png")
        self.open_icon = QIcon(":/icons/icons/pause.png")
        if status == 1:
            self.btn1.setIcon(self.close_icon)
        else:
            self.btn1.setIcon(self.open_icon)

        self.btn1.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn1.clicked.connect(self.toggle_icon)

        self.btn2 = QPushButton()
        self.btn2.setIcon(QIcon(":/icons/icons/stop.png"))
        self.btn2.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn2.clicked.connect(self.delete)
        # 简单样式
        for btn in (self.btn1, self.btn2):
            btn.setFixedSize(20, 20)  # 小按钮尺寸
            btn.setIconSize(QSize(16, 16))
            btn.setStyleSheet(
                """
                QPushButton {
                    background-color: transparent;
                    border: none;
                    padding: 0;
                    margin: 0;
                }
                QPushButton:hover {
                    background-color: rgba(0, 122, 255, 0.1);  /* 浅蓝 hover 效果 */
                    border-radius: 4px;
                }
                QPushButton:pressed {
                    background-color: rgba(0, 122, 255, 0.2);
                }
            """
            )
        layout.addWidget(self.btn1)
        layout.addWidget(self.btn2)

    def toggle_icon(self):

        current_icon = self.btn1.icon()
        if self.status == 0:
            print("暂停了")
            self.rowChanged.emit(self.parent().parent().objectName(), self.row, 1)
            self.btn1.setIcon(self.close_icon)
        else:
            self.btn1.setIcon(self.open_icon)
            self.rowChanged.emit(self.parent().parent().objectName(), self.row, 0)
            print("继续了")

    def delete(self):
        parent = self.parent()
        self.rowDeleted.emit(self.parent().parent().objectName(), self.row)


class ButtonReceivingWidget(QWidget):
    rowDeleted = Signal(str, int)

    def __init__(self, row, parent=None):
        super().__init__(parent)
        self.row = row
        layout = QHBoxLayout(self)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        self.btn2 = QPushButton()
        self.btn2.setIcon(QIcon(":/icons/icons/stop.png"))
        self.btn2.setCursor(QCursor(Qt.PointingHandCursor))
        self.btn2.clicked.connect(self.delete)
        self.btn2.setFixedSize(20, 20)  # 小按钮尺寸
        self.btn2.setIconSize(QSize(16, 16))
        self.btn2.setStyleSheet(
            """
            QPushButton {
                background-color: transparent;
                border: none;
                padding: 0;
                margin: 0;
            }
            QPushButton:hover {
                background-color: rgba(0, 122, 255, 0.1);  /* 浅蓝 hover 效果 */
                border-radius: 4px;
            }
            QPushButton:pressed {
                background-color: rgba(0, 122, 255, 0.2);
            }
        """
        )
        layout.addWidget(self.btn2)

    def delete(self):
        self.rowDeleted.emit(self.parent().parent().objectName(), self.row)
