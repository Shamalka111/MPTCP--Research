import re

def parse_iperf_output(file_path, output_data_file):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    with open(output_data_file, 'w') as data_file:
        data_file.write("# Time (seconds) Throughput (Gbits/sec)\n")
        
        for line in lines:
            match = re.search(r'\[\s*\d+\]\s+(\d+\.\d+)-(\d+\.\d+)\s+sec\s+(\d+\.\d+)\s+GBytes\s+(\d+\.\d+)\s+Gbits/sec', line)
            if match:
                end_time = float(match.group(2))
                throughput = float(match.group(4))
                data_file.write(f"{end_time} {throughput}\n")

# Path to the iperf output file
file_path = 'mptcp_en_output.txt'
# Path to the output data file for Gnuplot
output_data_file = 'mptcp_en_output_throughput_data.dat'
parse_iperf_output(file_path, output_data_file)
