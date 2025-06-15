import asyncio

from typing import Any, Callable, Optional

from PySide6.QtCore import QObject, Signal, Slot, QThread, Qt
from PySide6.QtWidgets import QApplication

from src.utils.logger import _logger


class AsyncDispatcher(QObject):
    finished = Signal(str)
    result_ready = Signal(object)

    def __init__(self, target: Any, max_concurrent_fire_tasks: int = 5):
        super().__init__()
        self._target = target
        self._task_queue = asyncio.Queue()
        self._running = False
        self._semaphore = asyncio.Semaphore(
            max_concurrent_fire_tasks
        )  # ✅ 控制并发的信号量

    async def _loop(self):
        self._running = True
        while self._running:
            coro_func, args, kwargs, future = await self._task_queue.get()
            _logger.info(
                f"Dispatcher received task: {coro_func.__name__} with args: {args}, kwargs: {kwargs}"
            )

            if future is not None:
                # ✅ 等待结果的任务：顺序执行并等待结果
                try:
                    result = await coro_func(*args, **kwargs)
                    future.set_result(result)
                    self.result_ready.emit(result)
                except Exception as e:
                    _logger.error(f"Error in dispatcher (await task): {e}")
                    future.set_exception(e)
                finally:
                    self._task_queue.task_done()
            else:
                # ✅ fire-and-forget 任务：并发执行
                asyncio.create_task(self._run_fire_and_forget(coro_func, args, kwargs))
                self._task_queue.task_done()

    async def _run_fire_and_forget(self, coro_func, args, kwargs):
        """受限并发执行 fire-and-forget 异步任务"""
        async with self._semaphore:
            try:
                await coro_func(*args, **kwargs)
            except Exception as e:
                _logger.error(f"Error in fire-and-forget task: {e}")

    def set_loop(self, loop: asyncio.AbstractEventLoop):
        self._loop = loop

    def dispatch(self, coro_func: Callable, *args, need_result: bool = False, **kwargs):
        if not hasattr(self, "_loop") or self._loop is None:
            raise RuntimeError("Event loop not set in AsyncDispatcher.")

        if need_result:
            # ✅ 需要结果：排队并同步返回 Future
            return asyncio.run_coroutine_threadsafe(
                self._queue_and_wait_with_future(coro_func, args, kwargs), self._loop
            )
        else:
            # ✅ fire-and-forget：并发排队
            asyncio.run_coroutine_threadsafe(
                self._queue_fire_and_forget(coro_func, args, kwargs), self._loop
            )
            return None

    async def _queue_and_wait_with_future(self, coro_func, args, kwargs):
        loop_future = asyncio.get_event_loop().create_future()
        await self._task_queue.put((coro_func, args, kwargs, loop_future))
        return await loop_future

    async def _queue_fire_and_forget(self, coro_func, args, kwargs):
        await self._task_queue.put((coro_func, args, kwargs, None))
        # 立即返回，任务在后台并发执行

    def stop(self):
        self._running = False
        try:
            # 不要 await，这里是主线程，使用线程安全的方式注入一个 noop 任务
            asyncio.run_coroutine_threadsafe(
                self._task_queue.put((self._noop, (), {}, None)), self._loop
            )
        except Exception as e:
            _logger.error(f"Error stopping dispatcher: {e}")

    async def _noop(self):
        pass


class DispatcherThread(QThread):
    def __init__(self, dispatcher: AsyncDispatcher):
        super().__init__()
        self.dispatcher = dispatcher
        self.loop: Optional[asyncio.AbstractEventLoop] = None  # 保存 loop

    def run(self):
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self.dispatcher._loop())

    def get_loop(self) -> Optional[asyncio.AbstractEventLoop]:
        return self.loop
