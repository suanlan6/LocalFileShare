from PySide6.QtWidgets import QDialog, QLabel, QVBoxLayout, QProgressBar
from PySide6.QtCore import Qt, QTimer


class LoadingDialog(QDialog):
    def __init__(self, parent=None, text="请稍候..."):
        super().__init__(parent)
        self.setWindowTitle("正在处理")
        self.setModal(True)
        self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
        self.setFixedSize(220, 100)

        layout = QVBoxLayout(self)

        self.label = QLabel(text)
        self.label.setAlignment(Qt.AlignCenter)

        self.progress = QProgressBar(self)
        self.progress.setRange(0, 0)  # 设置为“无限循环”模式
        self.progress.setTextVisible(False)
        self.progress.setFixedHeight(20)

        layout.addWidget(self.label)
        layout.addWidget(self.progress)
