import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Callable


class TaskExecutor:
    def __init__(self, max_workers: int = 4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.loop = asyncio.get_event_loop()

    def run_in_background(self, task: Callable, *args: Any, **kwargs: Any):
        if asyncio.iscoroutinefunction(task):
            self.loop.run_in_executor(
                self.executor, lambda: asyncio.run(task(*args, **kwargs))
            )
        else:
            self.loop.run_in_executor(self.executor, lambda: task(*args, **kwargs))

    def shutdown(self):
        self.executor.shutdown()