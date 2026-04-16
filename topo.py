from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController
from mininet.cli import CLI

class MyStaticTopo(Topo):
    def build(self):
        # Add Switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add Hosts
        h1 = self.addHost('h1', ip='10.0.0.1')
        h2 = self.addHost('h2', ip='10.0.0.2')
        h3 = self.addHost('h3', ip='10.0.0.3')

        # Connect Hosts to Switches (Port 1)
        self.addLink(h1, s1, port2=1)
        self.addLink(h2, s2, port2=1)
        self.addLink(h3, s3, port2=1)

        # Connect Switches (Linear Chain)
        self.addLink(s1, s2, port1=2, port2=2)
        self.addLink(s2, s3, port1=3, port2=2)

topos = {'mystatictopo': (lambda: MyStaticTopo())}
