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
throughput_scenario1 = parse_iperf_output('day5_dis_diff.txt')
throughput_scenario2 = parse_iperf_output('day5_en_diff.txt')
throughput_scenario3 = parse_iperf_output('day5_en_same9.txt')
throughput_scenario4 = parse_iperf_output('day5_en_same15.txt')

# Determine the length of the longest list
max_len = max(len(throughput_scenario1), len(throughput_scenario2), len(throughput_scenario3), len(throughput_scenario4))

# Pad the shorter lists with NaN values
throughput_scenario1 += [np.nan] * (max_len - len(throughput_scenario1))
throughput_scenario2 += [np.nan] * (max_len - len(throughput_scenario2))
throughput_scenario3 += [np.nan] * (max_len - len(throughput_scenario3))
throughput_scenario4 += [np.nan] * (max_len - len(throughput_scenario4))

# Create a DataFrame for plotting
data = {
    'Time (s)': range(max_len),
    'Scenario 1 Throughput (Mbits/sec)': throughput_scenario1,
    'Scenario 2 Throughput (Mbits/sec)': throughput_scenario2,
    'Scenario 3 Throughput (Mbits/sec)': throughput_scenario3,
    'Scenario 4 Throughput (Mbits/sec)': throughput_scenario4
}
df = pd.DataFrame(data)

# Plot throughput over time
plt.figure(figsize=(12, 6))
plt.plot(df['Time (s)'], df['Scenario 1 Throughput (Mbits/sec)'], label='TCP')
plt.plot(df['Time (s)'], df['Scenario 2 Throughput (Mbits/sec)'], label='MPTCP different MTU')
plt.plot(df['Time (s)'], df['Scenario 3 Throughput (Mbits/sec)'], label='MPTCP 9000 MTU')
plt.plot(df['Time (s)'], df['Scenario 4 Throughput (Mbits/sec)'], label='MPTCP 1500 MTU')
plt.xlabel('Time (s)')
plt.ylabel('Throughput (Mbits/sec)')
plt.title('Throughput Over Time - Different path MTU')
plt.legend()
plt.grid(True)
plt.show()

# Plot boxplot of throughput, ignoring NaN values
plt.figure(figsize=(8, 6))
plt.boxplot([df['Scenario 1 Throughput (Mbits/sec)'].dropna(), 
             df['Scenario 2 Throughput (Mbits/sec)'].dropna(), 
             df['Scenario 3 Throughput (Mbits/sec)'].dropna(),
             df['Scenario 4 Throughput (Mbits/sec)'].dropna()], 
            labels=['TCP', 'MPTCP different MTU', 'MPTCP 9000 MTU', 'MPTCP 1500 MTU'])
plt.ylabel('Throughput (Mbits/sec)')
plt.title('Throughput Distribution of Different MTU Subflow')
plt.grid(True)
plt.show()
