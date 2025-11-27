from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class SimpleTopo(Topo):
    def build(self):
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        s1 = self.addSwitch('s1')
        self.addLink(h1, s1)
        self.addLink(h2, s1)

def run():
    setLogLevel('info')
    topo = SimpleTopo()

    net = Mininet(topo=topo, controller=None, switch=OVSSwitch, link=TCLink)
    net.start()

    # Set switch in standalone mode (acts like learning switch)
    s1 = net.get('s1')
    s1.cmd('ovs-vsctl set-fail-mode s1 standalone')

    h1, h2 = net.get('h1'), net.get('h2')
    h1.setIP('10.0.0.1/8')
    h2.setIP('10.0.0.2/8')

    print("\nPing from h1 to h2:")
    print(h1.cmd('ping -c 3 10.0.0.2'))

    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()
