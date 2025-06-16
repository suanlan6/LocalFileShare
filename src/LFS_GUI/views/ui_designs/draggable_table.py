from PySide6.QtWidgets import QTableWidget, QAbstractItemView
from PySide6.QtCore import Qt, QMimeData, Signal
from PySide6.QtGui import QDropEvent


class DraggableTableWidget(QTableWidget):
    rowDropped = Signal(str, str, list)

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
                # 获取所有选中的行索引，去重后排序
                rows = sorted(set(item.row() for item in selected_items))
                self.rowDropped.emit(source.name, self.name, rows)
        elif source == self:
            print(f"内部拖放完成于 {self.name}")
