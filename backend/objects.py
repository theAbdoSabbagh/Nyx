from typing import Optional

class CPU:
    def __init__(
        self,
        processor: str,
        temperature: float,
        usage: float,
    ):
        self.processor = processor
        self.temperature = temperature
        self.usage = usage
    
    def __str__(self):
        return f"CPU: {self.processor} | Temperature: {self.temperature:.2f}C | Usage: {self.usage:.2f}%"

# GPU add name, temperature, usage and clock
class GPU:
    def __init__(
        self,
        name: str,
        temperature: float,
        usage: float,
        clock: float,
    ):
        self.name = name
        self.temperature = temperature
        self.usage = usage
        self.clock = clock
    
    def __str__(self):
        return f"GPU: {self.name} | Temperature: {self.temperature:.2f}C | Usage: {self.usage:.2f}% | Clock: {self.clock:.2f}MHz"

# Harddisk add name, total, free space
class Harddisk:
    def __init__(
        self,
        total: float,
        free: float,
        drive_type: str,
    ):
        self.total = total
        self.free = free
        self.used_percent = (total - free) / total * 100
        self.drive_type = drive_type
        # label must be like SSD (1 TB) or SSD (750 GB) or HDD (1 TB) etc
        self.labelized = f"{drive_type} ({total/1024:.0f} TB)" if total > 1024 else f"{drive_type} ({total:.0f} GB)"
    
    def __str__(self):
        return f"Drive type: {self.drive_type} | Total: {self.total:.2f}GB | Free: {self.free:.2f}GB | Used Space: {self.used_percent:.2f}% | Labelized: {self.labelized}"

# RAM add total, available, used and VRAM clock
class RAM:
    def __init__(
        self,
        total: float,
        available: float,
        used: float,
        clock: float,
    ):
        self.total = total
        self.available = available
        self.used = used
        self.used_percent = used / total * 100
        self.clock = clock
    
    def __str__(self):
        return f"RAM: Total: {self.total}GB | Available: {self.available:.2f}GB | Used: {self.used:.2f}GB | Used Percent: {self.used_percent:.2f}% | Clock: {self.clock:.2f}MHz"

class Row:
    def __init__(
        self,
        label_text: str,
        value_text: str,
        dark: bool,
        index: int,
    ):
        self.label_text = label_text
        self.value_text = value_text
        self.dark = dark
        self.index = index
    
    def __str__(self):
        return f"Row: {self.label_text} | {self.value_text} | {self.dark} | {self.index}"

class Network:
    def __init__(
        self,
        interface: str,
        download_speed: float,
        upload_speed: float,
        download_unit: str,
        upload_unit: str,
    ):
        self.interface = interface
        self.download_speed = download_speed
        self.upload_speed = upload_speed
        self.download_unit = download_unit
        self.upload_unit = upload_unit
        self.download_labelized = f"{download_speed} {download_unit}"
        self.upload_labelized = f"{upload_speed} {upload_unit}"

    def __str__(self):
        return f"Network: {self.interface} | Download Speed: {self.download_speed} {self.download_unit} | Upload Speed: {self.upload_speed} {self.upload_unit}"