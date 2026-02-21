import psutil
import threading
import time
from datetime import datetime

class PerformanceMonitor:
    @staticmethod
    def get_system_metrics() -> dict:
        """Reports system execution metrics"""
        process = psutil.Process()
        memory_usage = process.memory_info().rss / (1024 * 1024)  # Convert to MB
        
        return {
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3], # Format: HH:mm:ss.SSS
            "memory": f"{memory_usage:.2f} MB",
            "threads": threading.active_count()
        }