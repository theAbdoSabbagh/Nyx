from rich import print
from time import strftime

class Logger:
    def __init__(self):
        pass

    def log(self, message: str):
        """Logs a message to the console with a timestamp.
        
        Args:
        ---------
        message (str): The message to log.
        """
        print(f"[bold white][{strftime('%H:%M:%S')}][/bold white] {message}")
    
    def success(self, message: str):
        """Logs a success message to the console.

        Args:
        ---------
            message (str): The message to log.
        """
        self.log(f"[bold green][ SUCCESS ][/bold green] [bold white]{message}[/bold white]")
    
    def error(self, message: str):
        """Logs a error message to the console.

        Args:
        ---------
            message (str): The message to log.
        """
        self.log(f"[bold red][ ERROR ][/bold red] [bold white]{message}[/bold white]")
    
    def warning(self, message: str):
        """Logs a warning message to the console.

        Args:
        ---------
            message (str): The message to log.
        """
        self.log(f"[bold yellow][ WARNING ][/bold yellow] [bold white]{message}[/bold white]")
    
    def info(self, message: str):
        """Logs a info message to the console.

        Args:
        ---------
            message (str): The message to log.
        """
        self.log(f"[bold blue][ INFO ][/bold blue] [bold white]{message}[/bold white]")
    
    def debug(self, message: str):
        """Logs a debug message to the console.

        Args:
        ---------
            message (str): The message to log.
        """
        self.log(f"[bold black][ DEBUG ] {message}")
    
    def critical(self, message: str):
        """Logs a critical message to the console.

        Args:
        ---------
            message (str): The message to log.
        """
        self.log(f"[bold white on red][ CRITICAL ] [bold white]{message}[/bold white]")

    def custom(self, message: str, color: str):
        """Logs a custom message to the console.

        Args:
        ---------
            message (str): The message to log.
        """
        self.log(f"[bold {color}][ CUSTOM ][/bold {color}] [bold white]{message}[/bold white]")
