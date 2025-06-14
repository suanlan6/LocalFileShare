import asyncio

from typing import Callable

from PySide6.QtCore import QObject, Signal, Slot


class AsyncWorker(QObject):
    finished = Signal(str)

    def __init__(self, method: Callable = None, *args, **kwargs):
        super().__init__()
        self._method = method  # 自定义方法
        self._args = args
        self._kwargs = kwargs

    @Slot()
    def run(self):
        """入口函数：调用传入的异步方法"""
        if self._method is None:
            self.finished.emit("未指定方法")
            return

        result = asyncio.run(self._method(*self._args, **self._kwargs))
        self.finished.emit(str(result))
