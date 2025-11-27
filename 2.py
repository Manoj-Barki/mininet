from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.link import TCLink
from mininet.cli import CLI
from mininet.log import setLogLevel

class ThreeSwitchTopo(Topo):
    def build(self):
        # Add hosts
        h1 = self.addHost('h1')
        h2 = self.addHost('h2')
        h3 = self.addHost('h3')
        server = self.addHost('server')

        # Add switches
        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')

        # Add links between hosts and switches
        self.addLink(h1, s1)
        self.addLink(h2, s2)
        self.addLink(h3, s3)
        self.addLink(server, s2)

        # Add links between switches
        self.addLink(s1, s2)
        self.addLink(s2, s3)

def run():
    setLogLevel('info')
    topo = ThreeSwitchTopo()

    # No external controller, use switch standalone mode
    net = Mininet(topo=topo, controller=None, switch=OVSSwitch, link=TCLink)
    net.start()

    # Set switches in standalone mode
    for sw in net.switches:
        sw.cmd(f'ovs-vsctl set-fail-mode {sw.name} standalone')

    # Assign IP addresses to hosts
    net.get('h1').setIP('10.0.0.1/8')
    net.get('h2').setIP('10.0.0.2/8')
    net.get('h3').setIP('10.0.0.3/8')
    net.get('server').setIP('10.0.0.10/8')

    print("\n=== MAC addresses of hosts and switches ===")
    for node in ['h1', 'h2', 'h3', 'server', 's1', 's2', 's3']:
        print(f"\n{node} interfaces:")
        print(net.get(node).cmd('ifconfig -a'))

    print("\n=== IP addresses of hosts and server ===")
    for node in ['h1', 'h2', 'h3', 'server']:
        print(f"\n{node}:")
        print(net.get(node).cmd('ip addr show'))

    CLI(net)
    net.stop()

if __name__ == '__main__':
    run()
