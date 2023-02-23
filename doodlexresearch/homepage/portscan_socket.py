import sys
import time
import socket
import asyncio
from datetime import datetime

class PortScannerSocket:

    def __init__(self, **kwargs):

        # scanning parameters
        self.host = kwargs["host"]
        self.from_port = kwargs["fromport"]
        self.end_port = kwargs["endport"]
        self.port_range = []
        self.open_ports = []

    def prepare_ports_format(self):
        """
        Preparing the ports range depending on the submission 
        """

        if int(self.from_port) == 0:
            self.port_range.extend((1, int(self.end_port)))
        
        elif int(self.from_port) >= 1:
            self.port_range.extend((int(self.from_port), int(self.end_port)))

        else:
            self.port_range.extend((1, int(self.end_port)))

    def check_host_is_up(self):
        """
        Checking if the host is up, required prior the scan, returns T/F.
        Default port is 1
        """
        try:
            target = socket.gethostbyname(self.host) 
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            socket.setdefaulttimeout(1)
            result = s.connect_ex((target, 1))

            if result == 47:
                self.open_ports.append(['Error: Host is down', f'{self.host}', f'An error occured during the scan, firewall blocked the connection or host {self.host} is down.'])
                s.close()
                return False

            else:
                s.close()
                return True

        except Exception as e:
            self.open_ports.append(['Error: Host is down', f'{self.host}', f'An error occured during the scan, firewall blocked the connection or host {self.host} is down.'])
            return False

    def check_results(self):
        """
        If after scan the list is empty, appends the message
        """
        if len(self.open_ports) == 0:
            self.open_ports.append(['No open ports', f'{self.host}', f'There are no open ports from the given range {self.port_range[0]}: {self.port_range[1]}'])
        
        return self.open_ports

    
    ## >>> Originally wrote syncronious function
    def scan_ports(self):
        """
        Scanning ports with sockets. Used only for the local hosts
        """
        
        try:
            target = socket.gethostbyname(self.host) 

            # will scan ports between with the specified range
            for port in range(self.port_range[0], self.port_range[1]):
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                result = s.connect_ex((target,port))

                if result == 0:
                    self.open_ports.append([f'{port}', f'{self.host}', f'port is open'])
                    s.close()

        except Exception as e:
            self.open_ports.append(['Error: Host is down', f'{self.host}', f'An error occured during the scan, firewall blocked the connection or host {self.host} is down.'])
   
        s.close()

        return self.open_ports

    
if __name__ == '__main__':

    start_time = time.time()

    a = PortScannerSocket(adress='localhost', fromport='1', endport='65536')
    a.prepare_ports_format()
    status = a.check_host_is_up()

    if status:
        a.scan_ports()
        a.check_results()

    else:
        a.check_results()

    print(a.open_ports)
    print("--- %s seconds ---" % (time.time() - start_time))


