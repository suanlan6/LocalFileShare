from PySide6.QtWidgets import QDialog, QApplication
from PySide6.QtCore import QEventLoop, QTimer
import asyncio
from typing import Any


def wait_future_with_dialog(future: asyncio.Future, dialog: QDialog) -> Any:
    """
    在 QDialog 中等待 asyncio.Future 完成，期间主线程保持响应。
    future: asyncio.Future 异步任务
    dialog: QDialog loading 对话框（需手动关闭）
    """
    loop = QEventLoop()

    def on_done(_):
        loop.quit()

    future.add_done_callback(on_done)

    dialog.show()  # 显示等待框
    QTimer.singleShot(100, loop.exec)  # 启动本地事件循环，防止卡死

    result = future.result()  # 注意：此时 future 已完成
    dialog.accept()  # 关闭等待框
    return result
