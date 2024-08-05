#!/usr/bin/env python

from mininet.net import Mininet
from mininet.cli import CLI
from mininet.link import Link, TCLink,Intf
from subprocess import Popen, PIPE
from mininet.log import setLogLevel
from mininet.term import makeTerm


if '__main__' == __name__:

  setLogLevel('info')
  net = Mininet(link=TCLink)
  key = "net.mptcp.mptcp_enabled"
  value = 0
  p = Popen("sysctl -w %s=%s" % (key, value), shell=True, stdout=PIPE, stderr=PIPE)
  stdout, stderr = p.communicate()
  print ("stdout=",stdout,"stderr=", stderr)


  h1 = net.addHost('h1')
  h2 = net.addHost('h2')
  r1 = net.addHost('r1')

  net.addLink(r1,h1,cls=TCLink)
  net.addLink(r1,h1,cls=TCLink)
  net.addLink(r1,h2,cls=TCLink)

  net.build()

  r1.cmd("ifconfig r1-eth0 0")
  r1.cmd("ifconfig r1-eth1 0")
  r1.cmd("ifconfig r1-eth2 0")
  h1.cmd("ifconfig h1-eth0 0")
  h1.cmd("ifconfig h1-eth1 0")
  h2.cmd("ifconfig h2-eth0 0")

  r1.cmd("echo 1 > /proc/sys/net/ipv4/ip_forward")
  r1.cmd("ifconfig r1-eth0 10.0.0.1 netmask 255.255.255.0")
  r1.cmd("ifconfig r1-eth1 10.0.1.1 netmask 255.255.255.0")
  r1.cmd("ifconfig r1-eth2 10.0.2.1 netmask 255.255.255.0")
  h1.cmd("ifconfig h1-eth0 10.0.0.2 netmask 255.255.255.0")
  h1.cmd("ifconfig h1-eth1 10.0.1.2 netmask 255.255.255.0")
  h2.cmd("ifconfig h2-eth0 10.0.2.2 netmask 255.255.255.0")
  h1.cmd("ip rule add from 10.0.0.2 table 1")
  h1.cmd("ip rule add from 10.0.1.2 table 2")
  h1.cmd("ip route add 10.0.0.0/24 dev h1-eth0 scope link table 1")
  h1.cmd("ip route add default via 10.0.0.1 dev h1-eth0 table 1")
  h1.cmd("ip route add 10.0.1.0/24 dev h1-eth1 scope link table 2")
  h1.cmd("ip route add default via 10.0.1.1 dev h1-eth1 table 2")
  h1.cmd("ip route add default scope global nexthop via 10.0.0.1 dev h1-eth0")
  h2.cmd("ip rule add from 10.0.2.2 table 1")
  h2.cmd("ip route add 10.0.2.0/24 dev h2-eth0 scope link table 1")
  h2.cmd("ip route add default via 10.0.2.1 dev h2-eth0 table 1")
  h2.cmd("ip route add default scope global nexthop via 10.0.2.1 dev h2-eth0")

# Execute the commands within the xterm windows
  #r1.cmd('bash -c "sleep 1; xterm -e \'tcpdump -i r1-eth2 -w run4.pcap\' &"')
  h2.cmd('bash -c "sleep 1; xterm -e \'iperf -s -i 1\' &"')
  h1.cmd('bash -c "sleep 1; xterm -e \'iperf -c 10.0.2.2 -t 10 -i 1\' &"')
  #h1.cmd('bash -c "sleep 1; xterm -e \'iperf -c 10.0.2.2 -t 10 -i 1 > mptcp_en_output.txt\' &"')
  #h1.cmd('bash -c "sleep 1; xterm -e \'iperf -c 10.0.2.2 -t 10 -i 1 >> allouts.txt\' &"')

  CLI(net)

  net.stop()