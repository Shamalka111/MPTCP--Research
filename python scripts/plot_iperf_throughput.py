import re
import matplotlib.pyplot as plt

def parse_iperf_server_output(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    times = []
    throughputs = []
    
    for line in lines:
        # Regex to match the lines containing throughput information
        match = re.search(r'\[\s*\d+\]\s+(\d+\.\d+)-(\d+\.\d+)\s+sec\s+(\d+\.\d+)\s+GBytes\s+(\d+\.\d+)\s+Gbits/sec', line)
        if match:
            start_time = float(match.group(1))
            end_time = float(match.group(2))
            throughput = float(match.group(4))  # Throughput in Gbits/sec
            
            times.append(end_time)
            throughputs.append(throughput)
    
    return times, throughputs

def plot_throughput(times, throughputs):
    plt.figure(figsize=(10, 6))
    plt.plot(times, throughputs, marker='o', linestyle='-', color='b')
    plt.xlabel('Time (seconds)')
    plt.ylabel('Throughput (Gbits/sec)')
    plt.title('Throughput Over Time')
    plt.grid(True)
    plt.show()

# Path to the iperf server output file
file_path = 'iperf_server_output.txt'
times, throughputs = parse_iperf_server_output(file_path)
plot_throughput(times, throughputs)
