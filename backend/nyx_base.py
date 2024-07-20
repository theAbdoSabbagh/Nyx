import psutil, os, math, pynvml, time, winreg, ctypes

from .logger import Logger
from .objects import CPU, GPU, Harddisk, RAM, Network

class NyxBase:
    def __init__(self):
        self.logger = Logger()

    def get_cpu_temperature(self):
        """Get CPU temperature using powershell command.
        
        Returns:
        ----------
        float:
            CPU temperature in Celsius."""
        return float(
            os.popen(
                'powershell.exe "(Get-CimInstance -ClassName Win32_PerfFormattedData_Counters_ThermalZoneInformation -Namespace "root/CIMV2").HighPrecisionTemperature / 10 - 273.15"'
            ).read().strip()
        )

    def get_cpu_usage(self):
        """Get CPU usage using powershell command.
        
        Returns:
        ----------
        float:
            CPU usage in percentage."""
        
        try:
            output = os.popen(
                    'powershell.exe "(Get-CimInstance -ClassName Win32_Processor).LoadPercentage"'
                ).read().strip()
            usage = 0
            if len(output) > 0:
                usage = float(output)
            return usage
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving CPU usage: {e}")
            return 0

    def get_cpu_name(self):
        """Get CPU name.
        
        Returns:
        ----------
        str:
            CPU name."""
        # return cpuinfo.get_cpu_info()["brand_raw"]
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\CentralProcessor\0")
        return winreg.QueryValueEx(key, "ProcessorNameString")[0]

    def get_gpu_temperature(self):
        """Get GPU temperature using nvidia-smi command.
        
        Returns:
        ----------
        int:
            GPU temperature in Celsius."""
        try:
            output = os.popen('nvidia-smi --query-gpu=temperature.gpu --format=csv,noheader,nounits').read().strip()
            temperature = int(output)
            return temperature
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving GPU temperature: {e}")
            return 0
    
    def get_gpu_usage(self):
        """Get GPU usage using nvidia-smi command.
        
        Returns:
        ----------
        int:
            GPU usage in percentage."""
        try:
            output = os.popen('nvidia-smi --query-gpu=utilization.gpu --format=csv,noheader,nounits').read().strip()
            usage = 0
            if len(output) > 0:
                usage = float(output)
            return usage
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving GPU usage: {e}")
            return 0

    def get_gpu_clock(self):
        """Get GPU clock using nvidia-smi command.
        
        Returns:
        ----------
        int:
            GPU clock in MHz."""
        try:
            output = os.popen('nvidia-smi --query-gpu=clocks.gr --format=csv,noheader,nounits').read().strip()
            clock = int(output)
            return clock
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving GPU clock: {e}")
            return 0
    
    def get_gpu_name(self):
        """Get GPU name using nvidia-smi command.
        
        Returns:
        ----------
        str:
            GPU name."""
        try:
            output = os.popen('nvidia-smi --query-gpu=name --format=csv,noheader,nounits').read().strip()
            return output
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving GPU name: {e}")
            return "N/A"

    def get_cpu(self):
        """Get CPU object.
        
        Returns:
        ----------
        CPU:
            CPU object containing processor name, temperature and usage."""
        
        # We get the CPU temperature first because the CPU heats up
        # When other stuff is being executed, so we get the temperature first so it's accurate
        # Because after everything is done, the CPU temperature will be back to normal
        temperature = self.get_cpu_temperature()

        return CPU(
            processor = self.get_cpu_name(),
            temperature = temperature,
            usage = self.get_cpu_usage(),
        )
    
    def get_gpu(self):
        """Get GPU object.
        
        Returns:
        ----------
        GPU:
            GPU object containing name, temperature, usage and clock."""
        return GPU(
            name = self.get_gpu_name(),
            temperature = self.get_gpu_temperature(),
            usage = self.get_gpu_usage(),
            clock = self.get_gpu_clock(),
        )

    def get_harddisk_info(self):
        """Get hard disk information using os.popen PowerShell command.
        
        Returns:
        ----------
        Harddisk:
            Hard disk object."""
            
        try:
            power_shell_command = 'powershell.exe "Get-PhysicalDisk | Format-Table -AutoSize"'
            disk_info = os.popen(power_shell_command).read().strip()
            
            drive_type = "SSD" if "ssd" in disk_info.lower() else "HDD"
            
            partitions = psutil.disk_partitions()
            primary_partition = partitions[0]
            
            usage = psutil.disk_usage(primary_partition.mountpoint)
            total_gb = usage.total / (1024.0 ** 3)
            free_gb = usage.free / (1024.0 ** 3)
            
            harddisk = Harddisk(total_gb, free_gb, drive_type)
            return harddisk
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving hard disk information: {e}")
            return Harddisk(0, 0, "N/A")

    def get_disk_io_percentage(self):
        """Get disk I/O percentage using psutil.disk_io_counters().

        Returns:
        ----------
        float:
            Disk I/O percentage."""
        initial_counters = psutil.disk_io_counters()
        time.sleep(1)
        final_counters = psutil.disk_io_counters()
        if not final_counters or not initial_counters:
            return 0
        read_bytes_delta = final_counters.read_bytes - initial_counters.read_bytes
        write_bytes_delta = final_counters.write_bytes - initial_counters.write_bytes
        total_bytes = read_bytes_delta + write_bytes_delta
        io_speed = total_bytes / 1 # 1 second
        max_io_speed = 500 * 1024 * 1024  # 500 MB/s in bytes
        io_percentage = (io_speed / max_io_speed) * 100
        
        return io_percentage
    
    def get_ram_info(self):
        """Get RAM information using psutil.virtual_memory().
        
        Returns:
        ----------
        tuple:
            Tuple containing total, available and used RAM."""
        ram = psutil.virtual_memory()
        total = math.ceil(ram.total / (1024.0 ** 3))
        available = ram.available / (1024.0 ** 3)
        used = ram.used / (1024.0 ** 3)
        
        # Get VRAM clock
        vram_clock = os.popen('nvidia-smi --query-gpu=clocks.mem --format=csv,noheader,nounits').read().strip()

        return RAM(total, available, used, float(vram_clock))

    def get_fans(self):
        """Get fan speeds using the NVIDIA Management Library (pynvml).
        
        Returns:
        ----------
        list:
            A list of dictionaries containing fan speeds in percentage.
        """
        try:
            pynvml.nvmlInit()
            device_count = pynvml.nvmlDeviceGetCount()
            fans = []

            for i in range(device_count):
                handle = pynvml.nvmlDeviceGetHandleByIndex(i)
                fan_speed = pynvml.nvmlDeviceGetFanSpeed(handle)
                fans.append({'fan': i + 1, 'speed': fan_speed})
            
            pynvml.nvmlShutdown()
            return fans

        except pynvml.NVMLError as e:
            self.logger.error(f"An error occurred while retrieving fan speeds: {e}")
            return []

        except Exception as e:
            self.logger.error(f"An unexpected error occurred: {e}")
            return []

    def get_computer_model(self):
        """Get computer model using os.popen command.
        
        Returns:
        ----------
        str:
            Computer model."""
        try:
            key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"HARDWARE\DESCRIPTION\System\BIOS")
            model, _ = winreg.QueryValueEx(key, "SystemProductName")
            winreg.CloseKey(key)
            return model
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving computer model: {e}")
            return "N/A"
        
    def get_power_plan(self):
        """Get power plan using os.popen command.
        
        Returns:
        ----------
        str:
            Power plan."""
        try:
            power_plan = os.popen('powercfg /getactivescheme').read().strip()
            power_plan = power_plan[power_plan.find("(") + 1:power_plan.find(")")]
            return power_plan
        except Exception as e:
            self.logger.error(f"An error occurred while retrieving power plan: {e}")
            return "N/A"
        
    def get_network_speed(self, interface: str):
        """Get network speed using psutil.net_io_counters().

        Parameters:
        ----------
        interface: str
            Interface name.
        
        Returns:
        ----------
        tuple:
            Tuple containing download and upload speed."""
        net_io_1 = psutil.net_io_counters(pernic=True)[interface]
        time.sleep(1)
        net_io_2 = psutil.net_io_counters(pernic=True)[interface]

        sent_unit = "Bytes/s"
        sent_speed = (net_io_2.bytes_sent - net_io_1.bytes_sent)
        # Convert to KB or MB
        if sent_speed > 1024:
            sent_speed = sent_speed / 1024
            sent_unit = "KB/s"
        if sent_speed > 1024:
            sent_speed = sent_speed / 1024
            sent_unit = "MB/s"
        
        recv_unit = "Bytes/s"
        recv_speed = (net_io_2.bytes_recv - net_io_1.bytes_recv)
        # Convert to KB or MB
        if recv_speed > 1024:
            recv_speed = recv_speed / 1024
            recv_unit = "KB/s"
        if recv_speed > 1024:
            recv_speed = recv_speed / 1024
            recv_unit = "MB/s"

        return Network(interface, round(recv_speed, 1), round(sent_speed, 1), recv_unit, sent_unit)

    def get_dpi(self):
        """Get DPI settings using ctypes.windll command.

        Returns:
        ----------
        tuple:
            Tuple containing horizontal and vertical DPI."""
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        hdc = user32.GetDC(0)
        dpi_x = gdi32.GetDeviceCaps(hdc, 88)  # LOGPIXELSX
        dpi_y = gdi32.GetDeviceCaps(hdc, 90)  # LOGPIXELSY
        user32.ReleaseDC(0, hdc)
        
        return dpi_x

    def get_screen_resolution(self):
        """Get screen resolution using ctypes.windll command.

        Returns:
        ----------
        tuple:
            Tuple containing screen width and height."""
        user32 = ctypes.windll.user32
        gdi32 = ctypes.windll.gdi32
        hdc = user32.GetDC(0)
        physical_width = gdi32.GetDeviceCaps(hdc, 8)  # HORZRES
        physical_height = gdi32.GetDeviceCaps(hdc, 10)  # VERTRES
        logical_width = gdi32.GetDeviceCaps(hdc, 118)  # DESKTOPHORZRES
        logical_height = gdi32.GetDeviceCaps(hdc, 117)  # DESKTOPVERTRES
        user32.ReleaseDC(0, hdc)
        dpi_scaling_factor_x = logical_width / physical_width
        dpi_scaling_factor_y = logical_height / physical_height
        actual_width = int(physical_width * dpi_scaling_factor_x)
        actual_height = int(physical_height * dpi_scaling_factor_y)
        return actual_width, actual_height
