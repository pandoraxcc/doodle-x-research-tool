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
        self.scan_ports_keys = []
        self.scan_ports_values = {}
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
        self.nm.scan(hosts=self.host, arguments=f'-p {self.port_str}')


    def prepare_results(self):
        """
        Wrap results of the scan
        """
        for host in self.nm.all_hosts():

            for protocol in self.nm[host].all_protocols():

                self.scan_ports_keys = self.nm[host][protocol].keys()
                print(len(self.scan_ports_keys))
                print("######")
                self.scan_ports_values = self.nm[host][protocol].values()
                print(len(self.scan_ports_values))
                print("######")

                for port, state in zip(self.scan_ports_keys, self.scan_ports_values):
                    if state['state'] == 'open':
                        record = [f'{port}', f'{host}', f'port is open']
                        self.open_ports.append(record)


if __name__ == '__main__':
    start_time = time.time()

    a = PortScannerTool(host='192.168.1.1', fromport='1', endport='65535')
    a.prepare_port_format()

    status = a.check_host_is_up_ping()

    if status:
        a.scan_ports()
        a.prepare_results()
        a.check_results()

    else:
        a.check_results()
    print("--- %s seconds ---" % (time.time() - start_time))
       