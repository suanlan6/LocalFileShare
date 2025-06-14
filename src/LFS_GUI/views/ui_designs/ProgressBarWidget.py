from PySide6.QtWidgets import QWidget, QProgressBar, QVBoxLayout

class ProgressBarWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        self.progress.setTextVisible(True)
        self.progress.setFormat("%p%")

        layout = QVBoxLayout(self)
        layout.setContentsMargins(2, 2, 2, 2)
        layout.addWidget(self.progress)

    def set_value(self, val):
        self.progress.setValue(val)

    def value(self):
        return self.progress.value()
