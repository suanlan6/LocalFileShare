from PySide6.QtWidgets import (
    QPushButton, QDialog, QVBoxLayout, QLabel,
    QLineEdit, QDialogButtonBox, QTableWidget, QHBoxLayout, QSpacerItem, QSizePolicy
)
from PySide6.QtCore import Qt

class VerificationDialog(QDialog):
    def __init__(self, ip, parent=None):
        super().__init__(parent)
        self.setWindowTitle("安全验证")
        self.setFixedSize(360, 200)
        self.setStyleSheet("""
            QDialog {
                background-color: #f7f9fa;
                font-family: "Microsoft YaHei";
                font-size: 13px;
            }
            QLabel {
                font-size: 13px;
                font-weight: bold;
                color: #333333;
            }
            QLineEdit {
                border: 1px solid #dcdfe6;
                border-radius: 4px;
                padding: 6px;
                background-color: white;
            }
            QPushButton {
                background-color: #3385ff;
                color: white;
                border: none;
                border-radius: 4px;
                padding: 6px 16px;
            }
            QPushButton:hover {
                background-color: #2878f0;
            }
            QPushButton:pressed {
                background-color: #1a60d1;
            }
        """)

        layout = QVBoxLayout(self)

        self.tip_label = QLabel(f"为确保账号安全，请输入验证码以继续访问：")
        self.tip_label.setWordWrap(True)
        layout.addWidget(self.tip_label)

        self.ip_label = QLabel(f"<b>{ip}</b>")
        self.ip_label.setStyleSheet("color: #3385ff; margin-bottom: 10px;font-size: 13px;")
        layout.addWidget(self.ip_label)

        self.input = QLineEdit()
        self.input.setPlaceholderText("请输入验证码")
        layout.addWidget(self.input)

        # 按钮布局（右对齐）
        btn_layout = QHBoxLayout()
        btn_layout.addItem(QSpacerItem(40, 20, QSizePolicy.Expanding, QSizePolicy.Minimum))

        self.submit_btn = QPushButton("提交")
        self.submit_btn.clicked.connect(self.accept)
        self.cancel_btn = QPushButton("取消")
        self.cancel_btn.clicked.connect(self.reject)

        btn_layout.addWidget(self.cancel_btn)
        btn_layout.addWidget(self.submit_btn)

        layout.addLayout(btn_layout)

    def get_code(self):
        return self.input.text()