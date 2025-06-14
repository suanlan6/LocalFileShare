import asyncio

from typing import Any, Callable

from PySide6.QtCore import QObject, Signal, Slot

from src.utils.logger import _logger


# class AsyncWorker(QObject):
#     finished = Signal(str)

#     def __init__(self, method: Callable = None, *args, **kwargs):
#         super().__init__()
#         self._method = method  # 自定义方法
#         self._args = args
#         self._kwargs = kwargs

#     @Slot()
#     def run(self):
#         """入口函数：调用传入的异步方法"""
#         if self._method is None:
#             self.finished.emit("未指定方法")
#             return

#         result = asyncio.run(self._method(*self._args, **self._kwargs))
#         self.finished.emit(str(result))


class AsyncDispatcher(QObject):
    finished = Signal(str)  # 可用于通知任务完成
    result_ready = Signal(object)  # ✅ 新增：用于传出异步结果

    def __init__(self, target: Any):
        super().__init__()
        self._target = target
        self._task_queue = asyncio.Queue()
        self._running = False

    @Slot()
    def run(self):
        asyncio.run(self._loop())

    async def _loop(self):
        self._running = True
        while self._running:
            coro_func, args, kwargs, future = await self._task_queue.get()
            try:
                result = await coro_func(*args, **kwargs)
                if future:
                    future.set_result(result)
                self.result_ready.emit(result)  # ✅ 通知主线程
            except Exception as e:
                _logger.error(f"Error in dispatcher: {e}")
                if future:
                    future.set_exception(e)
            self._task_queue.task_done()

    def dispatch(self, coro_func: Callable, *args, **kwargs) -> asyncio.Future:
        loop = asyncio.get_event_loop()
        future = loop.create_future()
        self._task_queue.put_nowait((coro_func, args, kwargs, future))
        return future  # ✅ 可选择 return 或内部处理
