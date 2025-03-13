import psutil
import time
import statistics
import socket
from datetime import datetime

sampling_interval = 1  # Second
samples_per_minute = 60 // sampling_interval
minutes_per_batch = 1  # Average per x min
samples_per_batch = samples_per_minute * minutes_per_batch
server_name = socket.gethostname()
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"CPU_Usage_{server_name}_{timestamp}.txt"
cpu_samples = []
print(f"Monitoring CPU usage... Logging to {filename}. Press Ctrl+C to stop.")

try:
    with open(filename, "w") as file:
        file.write("Server Name, Timestamp, Batch Average (%), Std Dev (%)\n") 
        
        while True:
            cpu_usage = psutil.cpu_percent(interval=sampling_interval)
            cpu_samples.append(cpu_usage)
            if len(cpu_samples) >= samples_per_batch:
                batch_mean = statistics.mean(cpu_samples)
                batch_std_dev = statistics.stdev(cpu_samples) if len(cpu_samples) > 1 else 0.0
                batch_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                file.write(f"{server_name}, {batch_timestamp}, {batch_mean:.2f}, {batch_std_dev:.2f}\n")
                file.flush()  
                print(f"[{batch_timestamp}] Batch Average: {batch_mean:.2f}%, Std Dev: {batch_std_dev:.2f}%")
                cpu_samples = [] 
                
except KeyboardInterrupt:
    print("\nMonitoring stopped.")

