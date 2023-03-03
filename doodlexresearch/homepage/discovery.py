import nmap


class DiscoveryTool:
    

    def __init__(self, **kwargs):

        self.network_mask = kwargs["netmask"]
        self.nm = nmap.PortScanner()
        self.connected_devices = []
        self.connection_reason = []
        self.discovery_details = {}
        
        #tesing_data
        #self.discovery_details = {'nmap': {'command_line': 'nmap -oX - -n -sP 192.168.1.0/24', 'scaninfo': {}, 'scanstats': {'timestr': 'Thu Mar  2 09:11:08 2023', 'elapsed': '15.19', 'uphosts': '2', 'downhosts': '254', 'totalhosts': '256'}}, 'scan': {'192.168.1.1': {'hostnames': [{'name': '', 'type': ''}], 'addresses': {'ipv4': '192.168.1.1'}, 'vendor': {}, 'status': {'state': 'up', 'reason': 'syn-ack'}}, '192.168.1.2': {'hostnames': [{'name': '', 'type': ''}], 'addresses': {'ipv4': '192.168.1.2'}, 'vendor': {}, 'status': {'state': 'up', 'reason': 'conn-refused'}}}}
        #self.connected_devices = [['192.168.1.1', "connected"], ['192.168.1.2', "connected"]]



    def discover_host(self):
        """Start the scan of the host, get the results"""

        self.nm.scan(hosts=self.network_mask, arguments=f'-n -sP')

        for host in self.nm.all_hosts():
            self.connected_devices.append([host, f'connected'])

        return self.connected_devices

    def add_detailed_information(self):
        """Getting the connection identifiers, for ex., how it's identified the host was up"""

        self.discovery_details = self.nm._scan_result
        
        for connection_item in self.connected_devices:
            host = connection_item[0]
            self.connection_reason.append(self.discovery_details['scan'][host]['status']['reason'])

        return self.connection_reason

    def prepare_results(self):
        """Combine identified hosts and connection indetifiers"""

        for x in range(len(self.connected_devices)):
            self.connected_devices[x].append(self.connection_reason[x])
        return self.connected_devices


    def check_results(self):
        """Checking the results, wrapping the data"""

        if len(self.connected_devices) == 0:
            self.connected_devices.append(['Error: host is down', f'An error occured during the scan. Firewall blocked the connection or host {self.network_mask} is down.', f'None'])
        
        else:
            self.add_detailed_information()
            self.prepare_results()

        return self.connected_devices

    
if __name__ == '__main__':
    a = DiscoveryTool(netmask="192.168.1.0/24")
    a.discover_host()
    res = a.check_results()
    print(res)
