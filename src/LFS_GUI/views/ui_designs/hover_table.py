from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QTableWidget, QTableWidgetItem


from src.LFS_GUI.views.ui_designs.ButtonWidget import (
    ButtonReceivingWidget,
    ButtonSendingWidget,
)


class HoverableTable(QTableWidget):
    rowDeleted = Signal(str, int)
    rowChanged = Signal(str, int, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.data = None
        self.setMouseTracking(True)
        self.current_hover_row = -1
        self.original_texts = {}  # {row: text}
        self.parent = parent

    def mouseMoveEvent(self, event):
        index = self.indexAt(event.pos())
        if not index.isValid():
            self.restore_previous_row()
            return

        row = index.row()
        if row != self.current_hover_row:
            self.restore_previous_row()
            self.show_buttons_in_row(row)
            self.current_hover_row = row

        super().mouseMoveEvent(event)

    def leaveEvent(self, event):
        self.restore_previous_row()
        super().leaveEvent(event)

    def show_buttons_in_row(self, row):
        # 保存原始文本
        item = self.item(row, 1)
        if item:
            self.original_texts[row] = item.text()
            # 移除原始 item，防止文本重叠
            self.takeItem(row, 1)
        if self.objectName() == "FromSendingData":
            status = self.data[row]["status"]
            button_widget = ButtonSendingWidget(row, status, self)
        else:
            button_widget = ButtonReceivingWidget(row, self)

        if hasattr(button_widget, "rowDeleted"):
            button_widget.rowDeleted.connect(self.rowDeleted)
        if hasattr(button_widget, "rowChanged"):
            button_widget.rowChanged.connect(self.rowChanged)

        self.setCellWidget(row, 1, button_widget)

    def restore_previous_row(self):
        if self.current_hover_row >= 0:
            original_text = self.original_texts.get(self.current_hover_row, "")
            self.removeCellWidget(self.current_hover_row, 1)
            # 恢复文本项
            item = QTableWidgetItem(original_text)
            item.setTextAlignment(Qt.AlignCenter)
            self.setItem(self.current_hover_row, 1, item)
            self.current_hover_row = -1
