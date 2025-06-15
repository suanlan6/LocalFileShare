from PySide6.QtWidgets import QTableWidget, QAbstractItemView
from PySide6.QtCore import Qt, QMimeData, Signal
from PySide6.QtGui import QDropEvent


class DraggableTableWidget(QTableWidget):
    rowDropped = Signal(str, str, int)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.name = self.parent().objectName()
        self.setAcceptDrops(True)
        self.setDragEnabled(True)
        self.setDropIndicatorShown(True)
        self.setDragDropMode(QAbstractItemView.InternalMove)

    def dropEvent(self, event: QDropEvent):
        source = event.source()
        if isinstance(source, QTableWidget) and source != self:
            selected_items = source.selectedItems()
            if selected_items:
                row = selected_items[0].row()
                self.rowDropped.emit(source.name, self.name, row)
        elif source == self:
            # 同表格内部拖放
            print(f"内部拖放完成于 {self.name}")
