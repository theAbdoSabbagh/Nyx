import os, sys, yaml, time
from datetime import datetime

from .logger import Logger
from .timer import Timer

class ErrorDumper:
    def __init__(self, folder_path: str):
        with Timer(__class__.__name__):
            self.folder_path = folder_path

            self.logger = Logger()
            self.errors = 0

            self.create_folder()

    def create_folder(self):
        if not os.path.exists(self.folder_path):
            os.makedirs(self.folder_path)
            self.logger.info(f"Created folder: {self.folder_path}")

    def announce_error(self, error_text: str):
        bars_count = len([bar for bar in error_text.split("|") if bar == "|"])
        if bars_count != 2:
            for i in range(2 - bars_count):
                error_text += "|"

        args = error_text.split("|")
        level = args[0]
        text = args[1]
        
        try:
            function = getattr(self.logger, level.lower())
            function(f"{text}")
        except AttributeError:
            self.logger.error(f"Invalid log level: {level}")

    def dump_error(self, exception_type: str, error_text: str):
        self.announce_error(error_text)

        timestamp = datetime.now().strftime("%I:%M:%S %p")
        timestamp_name = datetime.now().strftime("%Y-%m-%d")
        file_name = f"error_log_{timestamp_name}.yaml"
        file_path = os.path.join(self.folder_path, file_name)

        data = {
            'error_text': error_text.split("|")[-1],
            'exception_type': exception_type,
        }

        with open(file_path, 'a') as file:
            yaml.dump({timestamp: [{key: value} for key, value in data.items()]}, file, default_flow_style=False)
            file.write("\n")

        self.logger.debug(f"Error dumped to file: {file_path}")
