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
        self.network_classes = {"classA": 10, "classB": 172, "classC": 192}
        # the list of ips for geo-lookup
        self.ips = []
        # geo-location details
        self.geo_location = []


    def process_traceroute(self):
        """Perfoming initial traceroute"""
        if self.target_ip:
            self.raw_data = os.popen(f"traceroute -w 1 -q 1 {self.target_ip}").readlines()
        else:
            self.raw_data = ["none"]
        return self.raw_data


    def oranize_data(self):
        """Clearing up the data after initial traceroute"""
        if len(self.raw_data) > 1:
            self.clean_data = [item.split(" ") for item in self.raw_data ]
            
            # clearing the empty records per hop
            for item in self.clean_data:
                for index, data in enumerate(item):
                    if data == '':
                        item.pop(index)
                # removing ms string from the record
                if len(item) > 2:
                    item.pop(-1)
                    # removing parentheses from the ip adress, 2nd element of the list
                    item[2] = item[2].replace('(','').replace(')','')

        else:
            self.clean_data = ["none"]
            print("\n Warning: raw data is missing. Run process_traceroute method first \n")
        
        return self.clean_data


    def define_network_class(self):
        """Based on the traceroute details, detect the local adress and append to the clean data"""
        if len(self.clean_data) > 1:

            for item in self.clean_data:
                if len(item) > 2:
                    ip_addr = int(item[2].split(".")[0])

                    if ip_addr >=1:
                        for ip_range in self.network_classes.values():
                            if int(ip_range) == ip_addr:
                                item.append("local-adress")
        return self.clean_data
    
    def get_ip_addrs(self):
        """Get the scanned ips for futher evaluation"""
        if len(self.clean_data) > 1:
            # get the list of the targeted IPs
            self.ips = [record[2] for record in self.clean_data if len(record) > 2 and 'local-adress' not in record]
        else:
            self.ips = ["none"]
        return self.ips


class Async_calls(Traceroute):

    def perform_traceroute(self):
        self.process_traceroute()
        self.oranize_data()
        self.define_network_class()
        self.get_ip_addrs()


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
        


if __name__ == '__main__':
    
    a = Async_calls("google.com")
    a.perform_traceroute()
    asyncio.run(a.main_calls())
    a.map_data()


