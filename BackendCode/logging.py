# Written by chatGPT cause I don't know shit about warnings.

import warnings
import functools
from pathlib import Path

def log_warnings(log_file="warnings.log"):
    """
    Decorator that captures all warnings during the wrapped function
    and appends them to the specified log file.
    """
    log_path = Path(log_file)

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            with warnings.catch_warnings(record=True) as caught_warnings:
                warnings.simplefilter("always")  # capture all warnings
                result = func(*args, **kwargs)

                # Append captured warnings to the log file
                if caught_warnings:
                    with log_path.open("a", encoding="utf-8") as f:
                        for w in caught_warnings:
                            f.write(
                                f"[{w.category.__name__}] {w.message} "
                                f"(from {w.filename}:{w.lineno})\n"
                            )

                return result

        return wrapper

    return decorator
