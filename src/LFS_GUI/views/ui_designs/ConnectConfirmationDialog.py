import random
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QSpacerItem,
    QSizePolicy,
)
from PySide6.QtCore import Qt


from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QLineEdit,
    QHBoxLayout,
    QSizePolicy,
)
from PySide6.QtCore import (
    Qt,
    Signal,
)


class ConnectConfirmationDialog(QDialog):
    confirmed = Signal()
    rejected = Signal()

    def __init__(self, controller, ip, pin_code, parent=None):
        super().__init__(parent)
        self.ip = ip
        self.controller = controller
        self.pin_code = pin_code
        self.connected = False
        self.setWindowTitle("连接确认")
        self.setFixedSize(320, 180)
        self.setStyleSheet(
            """
            QDialog {
                background-color: white;
                border-radius: 12px;
                font-family: 'Microsoft YaHei', 'PingFang SC', sans-serif;
                font-size: 14px;
                color: #333333;
            }
            QLabel#titleLabel {
                font-size: 18px;
                font-weight: 600;
                color: #2d8cf0;
            }
            QLabel#infoLabel {
                font-size: 13px;
                color: #666666;
                margin-top: 8px;
            }
            QPushButton {
                background-color: #2d8cf0;
                border: none;
                color: white;
                font-size: 14px;
                font-weight: 600;
                border-radius: 6px;
                min-height: 36px;
                padding: 0 20px;
            }
            QPushButton:hover {
                background-color: #66a8ff;
            }
            QPushButton:disabled {
                background-color: #a0cfff;
            }
            QLineEdit {
                border: 1px solid #d9d9d9;
                border-radius: 6px;
                padding: 6px 10px;
                font-size: 14px;
                color: #333333;
                margin-top: 12px;
                min-height: 32px;
            }
            QLineEdit:focus {
                border-color: #2d8cf0;
                outline: none;
            }
        """
        )

        # 主垂直布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.setSpacing(12)

        # 标题
        self.titleLabel = QLabel(f"请求连接：{self.ip}")
        self.titleLabel.setObjectName("titleLabel")
        layout.addWidget(self.titleLabel, alignment=Qt.AlignCenter)

        # 提示信息
        self.infoLabel = QLabel("是否同意连接？点击同意后会显示验证码。")
        self.infoLabel.setObjectName("infoLabel")
        self.infoLabel.setWordWrap(True)
        layout.addWidget(self.infoLabel, alignment=Qt.AlignCenter)

        # 验证码输入行（隐藏，等待同意后显示）
        self.codeLineEdit = QLineEdit()
        self.codeLineEdit.setPlaceholderText("验证码")
        self.codeLineEdit.setMaxLength(4)
        self.codeLineEdit.setVisible(False)
        layout.addWidget(self.codeLineEdit)

        # 按钮布局
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(16)

        self.agreeBtn = QPushButton("同意")
        self.cancelBtn = QPushButton("取消")

        btn_layout.addWidget(self.cancelBtn)
        btn_layout.addWidget(self.agreeBtn)

        layout.addLayout(btn_layout)

        # 信号绑定
        self.agreeBtn.clicked.connect(self.on_agree)
        self.cancelBtn.clicked.connect(self.on_cancel)

    def on_agree(self):
        # 显示验证码，删除取消按钮
        self.infoLabel.setText(f"验证码：{self.pin_code}")
        self.codeLineEdit.setVisible(False)
        self.cancelBtn.hide()
        self.agreeBtn.hide()
        self.connected = True
        self.confirmed.emit()

    def on_cancel(self):
        print("hello")
        self.reject()
        self.rejected.emit()
