#!/usr/bin/env python
# author = 'ZZH'
# time = 2023/12/29
# project = common
import functools
from loguru import logger
import time

def retry(retry_times, default=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for _ in range(retry_times):
                try:
                    output = func(*args, **kwargs)
                    return output if output is not None else default
                except Exception as e:
                    logger.warning(f"Function execution failed, retrying... {e}")
                    time.sleep(30)

            raise Exception("Function execution failed after multiple retries.")

        return wrapper

    return decorator