from time import time
from .logger import Logger

class Timer:
    def __init__(self, class_name: str):
        self.class_name = class_name

    def __enter__(self):
        self.start_time = time()
        self.logger = Logger()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed_time = time() - self.start_time
        self.logger.debug(f"Finished initializing {self.class_name} in {elapsed_time:.2f}s")
