# File: plot_iperf_throughput.gnuplot

set terminal png size 800,600
set output 'mptcp_en_output_throughput.png'
set title "Throughput Over Time"
set xlabel "Time (seconds)"
set ylabel "Throughput (Gbits/sec)"
set grid
plot 'mptcp_en_output_throughput_data.dat' using 1:2 with linespoints title "Throughput"
