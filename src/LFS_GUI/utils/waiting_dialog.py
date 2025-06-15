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

    def check_future():
        if future.done():
            loop.quit()
        else:
            QTimer.singleShot(100, check_future)  # 继续检查

    future.add_done_callback(lambda _: None)  # 可以不做事，只是确保 future 被监控

    dialog.show()
    QTimer.singleShot(0, check_future)  # 立即开始检查
    loop.exec()  # 阻塞直到 quit()

    # future 已完成
    result = future.result()
    dialog.accept()
    return result
