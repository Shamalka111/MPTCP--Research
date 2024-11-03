#!/usr/bin/python

from mininet.net import Mininet
from mininet.node import Node
from mininet.topo import Topo
from mininet.link import Link, TCLink
from mininet.log import setLogLevel, info
from mininet.cli import CLI

class CustomTopo(Topo):
    def build(self):
        # Add hosts and router
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        r1 = self.addHost('r1')

        # Create links with custom MTUs
        self.addLink(h1, r1, intfName1='h1-eth0', intfName2='r1-eth0', cls=TCLink)
        self.addLink(h2, r1, intfName1='h2-eth0', intfName2='r1-eth1', cls=TCLink)

def run():
    topo = CustomTopo()
    net = Mininet(topo=topo, link=TCLink)
    net.start()

    # Configure IP addresses
    net['h1'].cmd('ifconfig h1-eth0 10.0.1.1/24')
    net['h2'].cmd('ifconfig h2-eth0 10.0.2.1/24')
    net['r1'].cmd('ifconfig r1-eth0 10.0.1.254/24')
    net['r1'].cmd('ifconfig r1-eth1 10.0.2.254/24')

    # Configure routing
    net['h1'].cmd('ip route add default via 10.0.1.254')
    net['h2'].cmd('ip route add default via 10.0.2.254')
    net['r1'].cmd('echo 1 > /proc/sys/net/ipv4/ip_forward')

    # Set MTUs for each interface
    net['h1'].cmd('ifconfig h1-eth0 mtu 9000')
    net['h2'].cmd('ifconfig h2-eth0 mtu 9000')
    net['r1'].cmd('ifconfig r1-eth0 mtu 1500')
    net['r1'].cmd('ifconfig r1-eth1 mtu 9000')

    # Run iperf test from h1 to h2
    net['h2'].cmd('bash -c "sleep 1; xterm -e \'iperf -s -i 1\' &"')
    net['h1'].cmd('bash -c "sleep 1; xterm -e \'iperf -c 10.0.2.1 -M 9000 -d -i 1\' &"')

    # Start CLI for further interaction
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel('info')
    run()