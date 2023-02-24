import nmap
import time
from .portscan_socket import PortScannerSocket

class PortScannerTool(PortScannerSocket):
    
    def __init__(self, **kwargs):

        # scanning parameters
        self.host = kwargs["host"]
        self.from_port = kwargs["fromport"]
        self.end_port = kwargs["endport"]
        self.port_str = ""
        self.open_ports_nmap = []
        self.open_ports = []
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
        self.nm.scan(hosts=self.host, arguments=f'-p {self.port_str}', timeout=10)

    def prepare_results(self):
        """
        Wrap results of the scan
        """
        for host in self.nm.all_hosts():

            for protocol in self.nm[host].all_protocols():

                self.open_ports_nmap = self.nm[host][protocol].keys()

                if len(self.open_ports_nmap) > 1:

                    for port in self.open_ports_nmap:
                        record = [f'{port}', f'{host}', f'port is open']
                        self.open_ports.append(record)

                else:
                    self.open_ports.append(['No open ports', f'{host}', f'There are no open ports from the given range {self.from_port}: {self.end_port}'])

        return self.open_ports    

if __name__ == '__main__':
    start_time = time.time()

    a = PortScannerTool(host='172.20.10.1', fromport='1', endport='65535')
    a.prepare_port_format()

    status = a.check_host_is_up()

    if status:
        a.scan_ports()
        res = a.prepare_results()

    else:
        a.check_results()

    print(a.open_ports)
    print("--- %s seconds ---" % (time.time() - start_time))
       