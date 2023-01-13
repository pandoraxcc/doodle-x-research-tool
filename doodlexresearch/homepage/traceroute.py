import asyncio
import aiohttp
import os
import requests

class Traceroute:

    def __init__(self , target_ip):
        # used for traceroute
        self.target_ip = target_ip
        # results after running traceroute
        self.raw_data = []
        # formatting the response after running traceroute
        self.clean_data = []
        # what defined as "local network"
        self.network_classes = {"classA": "10", "classB": "172.16", "classC": "192.168"}
        # the list of ips for geo-lookup
        self.ips = []
        # geo-location details
        self.geo_location = []


    def process_traceroute(self):
        """
        Perfoming initial traceroute
        """
        if self.target_ip:
            self.raw_data = os.popen(f"traceroute -w 1 -q 1 {self.target_ip}").readlines()
        else:
            self.raw_data = ["none"]
        return self.raw_data


    def oranize_data(self):
        """
        Clearing up the data after initial traceroute
        """
        if len(self.raw_data) > 1:
            self.clean_data = [item.split(" ") for item in self.raw_data ]
            
            # clearing the empty records per hop
            for item in self.clean_data:
                print('\n')
                print(item)
                print('\n')
                for index, data in enumerate(item):
                    # removing the empty elements
                    if data == '':
                        item.pop(index)
                    # removing ms string from the record
                    if 'ms' in data:
                        item.pop(index)
                        
                if len(item) > 2:
                    # removing parentheses from the ip adress
                    item[2] = item[2].replace('(','').replace(')','')

        else:
            self.clean_data = ["none"]
            print("\n Warning: raw data is missing. Run process_traceroute method first \n")
        
        return self.clean_data


    def define_network_class(self):
        """
        Based on the traceroute details, 
        Detect the public or private adress and append to the clean data
        """
        if len(self.clean_data) > 1:
            class_ip_vals = self.network_classes.values()
            class_ip_vals = [item.split(".") for item in class_ip_vals]

            for item in self.clean_data:

                if len(item) > 2:

                    # getting the octets 
                    ip_addr = (item[2].split("."))

                    if len(ip_addr) >=1:
                        
                        #Checking class A
                        if ip_addr[0] == class_ip_vals[0][0]:
                            item.append("private-adress")
                        
                        # Checking class B
                        elif ip_addr[0] == class_ip_vals[1][0]:
                            if int(ip_addr[1]) >= 16 and int(ip_addr[1]) <= 31:
                                item.append("private-adress")
                            else:
                                item.append("public-adress")
                        
                        # Checking class C
                        elif ip_addr[0] == class_ip_vals[2][0]:
                            if int(ip_addr[1]) == 168:
                                item.append("private-adress")
                            else:
                                item.append("public-adress")
                        
                        # For the rest of Ips
                        else:
                            item.append("public-adress")
            
            for item in self.clean_data:
                if "private-adress" in item:
                    item.append("No location data")


        return self.clean_data
    

    def get_ip_addrs(self):
        """Get the scanned ips for futher evaluation"""
        if len(self.clean_data) > 1:
            # get the list of the targeted IPs
            self.ips = [record[2] for record in self.clean_data if len(record) > 2 and 'private-adress' not in record]
        else:
            self.ips = ["none"]
        return self.ips


    def count_stars(self):
        """
        If we got * in the traceroute:
        we set the values as none for the rest of the columns
        """
        empty_vals = ["none", "none", "none", "none"]
        for array in self.clean_data:
            for item in array:
                if "*\n" in item:
                    array.extend(empty_vals)
                    break


class Async_calls(Traceroute):

    def perform_traceroute(self):
        self.process_traceroute()
        self.oranize_data()
        self.define_network_class()
        self.get_ip_addrs()
        self.count_stars()


    async def get_location(self, ip, session, endpoint):
        """Create a task with the request from the passed ip address"""
        if len(self.clean_data) > 1:

            async with session.get(endpoint) as response:
                ip_info = await response.json()
                ip_info = {
                            "ip": ip,
                            "country": ip_info.get("country_name"),
                            "city": ip_info.get("city"),
                            "region": ip_info.get("region"),
                            "country_area": ip_info.get("country_area"),
                            "organization": ip_info.get("org")
                            }

                return ip_info

    async def main_calls(self):
        """Add the tasks to the loop and gathers the responses"""
        async with aiohttp.ClientSession() as session:
            tasks = []

            for country_ip in self.ips:
                endpoint = f'https://ipapi.co/{country_ip}/json/'
                tasks.append(asyncio.ensure_future(self.get_location(country_ip, session, endpoint)))

            self.geo_location = await asyncio.gather(*tasks)

    def map_data(self):
        """Add geo-location with matched ip addresses"""
        for row in self.clean_data:
            for item in self.geo_location:
                if item.get('ip') in row:
                    item.pop('ip')
                    row.append(item)
                    break
        return self.clean_data
        


if __name__ == '__main__':
    
    a = Async_calls("google.com")
    a.perform_traceroute()
    asyncio.run(a.main_calls())
    a.map_data()



