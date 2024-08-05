#!/bin/bash
make
sudo rmmod -f balia1.ko
sudo insmod balia1.ko

cc=$(< /proc/sys/net/ipv4/tcp_allowed_congestion_control)
cc="$balia1"
sudo sysctl net.ipv4.tcp_allowed_congestion_control=$cc

#end
