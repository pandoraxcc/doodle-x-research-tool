import nmap

class PortScannerTool:
    
    def __init__(self, **kwargs):

        # scanning parameters
        self.host = kwargs["adress"]
        self.from_port = kwargs["fromport"]
        self.end_port = kwargs["endport"]
        self.port_str = ""
        self.open_ports = []
        self.result = []
        self.nm = nmap.PortScanner()


    def prepare_port_format(self):
        """
        Preparing the argument for port scanner
        """
        if self.from_port == '0':
            self.port_str = self.end_port
        else:
            self.port_str = self.from_port + "-" + self.end_port


    def scan_ports(self):
        """
        Scan for open ports
        """
        self.nm.scan(hosts=self.host, ports=self.port_str)

    def prepare_results(self):
        """
        Wrap results of the scan
        """
        for host in self.nm.all_hosts():

            for protocol in self.nm[host].all_protocols():
                self.open_ports = self.nm[host][protocol].keys()

                if len(self.open_ports) > 1:

                    for port in self.open_ports:
                        record = {'port': port, 'state': self.nm[host][protocol][port]['state']}
                        self.result.append(record)

                else:
                    record = {'status': 'no open ports'}
                    self.result.append(record)

        return self.result    

if __name__ == '__main__':
    a = PortScannerTool(adress='0.0.0.0', fromport='1', endport='65535')
    a.prepare_port_format()
    a.scan_ports()
    res = a.prepare_results()
    print(res)
        