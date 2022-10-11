import threading
import functools

lock = threading.Lock()

class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """Function to ensure that any class with the metaclass "Singleton" can only be instantiated once.
        Uses a "check-lock-check" pattern to ensure this across threads.
        """
        if cls not in cls._instances:
            with lock:
                if cls not in cls._instances:
                    cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
