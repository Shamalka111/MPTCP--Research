import re

def parse_iperf_output(file_path, output_data_file):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    with open(output_data_file, 'w') as data_file:
        data_file.write("# Time (seconds) Throughput (Gbits/sec)\n")
        
        for line in lines:
            # Updated regex to handle both GBytes and MBytes
            match = re.search(r'\[\s*\d+\]\s+(\d+\.\d+)-(\d+\.\d+)\s+sec\s+(\d+\.?\d*)\s+([GM]Bytes)\s+(\d+\.?\d*)\s+([GM]bits/sec)', line)
            if match:
                start_time = float(match.group(1))
                end_time = float(match.group(2))
                transfer_amount = float(match.group(3))
                transfer_unit = match.group(4)
                throughput = float(match.group(5))
                throughput_unit = match.group(6)
                
                # Convert MBytes to GBytes and Mbits/sec to Gbits/sec if necessary
                if transfer_unit == "MBytes":
                    transfer_amount /= 1024
                if throughput_unit == "Mbits/sec":
                    throughput /= 1000
                
                data_file.write(f"{end_time} {throughput}\n")

# Path to the iperf output file
file_path = 'mptcp_en_output.txt'
# Path to the output data file for Gnuplot
output_data_file = 'mptcp_en_output_throughput_data.dat'
parse_iperf_output(file_path, output_data_file)
