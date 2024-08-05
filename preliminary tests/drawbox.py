import pandas as pd
import matplotlib.pyplot as plt
import re
import numpy as np

def parse_iperf_output(filename):
    """
    Parses the iperf3 output file to extract the throughput data.
    Assumes the file contains lines with 'sec' and 'Mbits/sec'.
    """
    throughput = []
    with open(filename, 'r') as file:
        for line in file:
            # Regex to match lines with throughput info
            match = re.search(r'(\d+.\d+)\s*Mbits/sec', line)
            if match:
                throughput.append(float(match.group(1)))
    return throughput

# Parse the iperf3 output files
throughput_scenario1 = parse_iperf_output('day4_dis.txt')
throughput_scenario2 = parse_iperf_output('day4_en.txt')

# Determine the length of the longer list
max_len = max(len(throughput_scenario1), len(throughput_scenario2))

# Pad the shorter list with NaN values
throughput_scenario1 += [np.nan] * (max_len - len(throughput_scenario1))
throughput_scenario2 += [np.nan] * (max_len - len(throughput_scenario2))

# Create a DataFrame for plotting
data = {
    'Time (s)': range(max_len),
    'Scenario 1 Throughput (Mbits/sec)': throughput_scenario1,
    'Scenario 2 Throughput (Mbits/sec)': throughput_scenario2
}
df = pd.DataFrame(data)

# Plot throughput over time
plt.figure(figsize=(12, 6))
plt.plot(df['Time (s)'], df['Scenario 1 Throughput (Mbits/sec)'], label='TCP')
plt.plot(df['Time (s)'], df['Scenario 2 Throughput (Mbits/sec)'], label='MPTCP')
plt.xlabel('Time (s)')
plt.ylabel('Throughput (Mbits/sec)')
plt.title('Throughput Over Time')
plt.legend()
plt.grid(True)
plt.show()

# Plot boxplot of throughput, ignoring NaN values
plt.figure(figsize=(8, 6))
plt.boxplot([df['Scenario 1 Throughput (Mbits/sec)'].dropna(), df['Scenario 2 Throughput (Mbits/sec)'].dropna()], labels=['TCP', 'MPTCP'])
plt.ylabel('Throughput (Mbits/sec)')
plt.title('Throughput Distribution of Different MTU Subflow')
plt.grid(True)
plt.show()
