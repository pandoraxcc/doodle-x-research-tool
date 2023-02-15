import sys
import socket
from datetime import datetime

class PortScannerSocket:

    def __init__(self, **kwargs):

        # scanning parameters
        self.host = kwargs["adress"]
        self.from_port = kwargs["fromport"]
        self.end_port = kwargs["endport"]
        self.port_range = []
        self.open_ports = []

    def prepare_ports_format(self):

        if int(self.from_port) == 0:
            self.port_range.extend((1, int(self.end_port)))
        
        elif int(self.from_port) >= 1:
            self.port_range.extend((int(self.from_port), int(self.end_port)))

        else:
            self.port_range.extend((1, int(self.end_port)))

    def scan_ports(self):

        try:
            target = socket.gethostbyname(self.host) 

            # will scan ports between with the specified range
            for port in range(self.port_range[0], self.port_range[1]):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                # default timeout for the client is 30 min
                # timeout when submitting multiple requests causing TimeOut Exception
                #socket.setdefaulttimeout(1)
                
                result = s.connect_ex((target,port))

                if result == 0:
                    self.open_ports.append([f'{port}', f'{self.host}', f'port is open'])
                s.close()

            if len(self.open_ports) == 0:
               self.open_ports.append(['No open ports', f'{self.host}', f'There are no open ports from the given range {self.port_range[0]}: {self.port_range[1]}'])
               

        except Exception as e:
            self.open_ports.append(['Error: Host is down', f'{self.host}', f'An error occured during the scan, firewall blocked the connection or host {self.host} is down.'])

        return self.open_ports

if __name__ == '__main__':
    a = PortScannerSocket(adress='0.0.0.0', fromport='1', endport='65535')
    a.prepare_ports_format()
    res = a.scan_ports()
