from concurrent.futures import ThreadPoolExecutor

from app.config import settings

# Thread pool executor for blocking I/O operations
executor: ThreadPoolExecutor | None = None


def get_executor() -> ThreadPoolExecutor:
    """Get the global thread pool executor instance"""
    if executor is None:
        raise RuntimeError("Executor not initialized")
    return executor


def initialize_executor():
    """Initialize the global thread pool executor instance"""
    global executor

    # Initialize thread pool executor
    executor = ThreadPoolExecutor(max_workers=settings.executor_max_workers)


def cleanup_executor():
    """Cleanup the global thread pool executor instance"""
    global executor

    # Shutdown executor
    executor.shutdown(wait=True)
