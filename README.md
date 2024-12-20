# Doodle-x-research-tool
Web app that visualizes and performs network scans. </br>I work on this project as a part of my constant learning about security and web development.</br></br>

## How to run the tool
1.You need to have python installed, verify installation: `python3 --version`</br>
2.Create a project folder: `cd ~/Desktop && mkdir cyber-tool`</br>
3.Clone the repository: `git clone https://github.com/pandoraxcc/doodle-x-research-tool.git`</br>
4.Create virtual enviroment: `python3 -m venv d-cyber` and activate it `source d-cyber/bin/activate`</br>
5.Install the requirements: `pip3 install -r requirements.txt`</br></br>

6.Download nmap library for python (developer's resource): curl -O https://xael.org/pages/python-nmap-0.7.1.tar.gz && tar -xzf python-nmap-0.7.1.tar.gz</br>
7.Verify the md5sum and add the library to the enviroment</br>
8.Update the database with a migration: python3 manage.py migrate</br> 
9.Run the server: `python3 manage.py runserver`</br>
10.Open the browser and navigate to 127.0.0.1:8000</br></br>

## Implementation of traceroute (completed)

Performs traceroute and unloads detailed information with stats graphs using Charts.js</br></br>

### Features:
1.Processes the traceroute with detailed stats, including: country, city, region, country area, ISP/organization by performing async requests to third party API</br>
2.Builds different graphs and charts based on the traceroute results: ping, organization, type of IP adress and countries.</br></br>

## Implementation of port scan (completed)
Updates: I decided to use sockets for the local scans, and nmap solution for non-local hosts. Nmap package seems to detect at better accuracy rather than custom written async socket scanner. However, perfomace based, I found it quite slow, so that requires improvement.</br>
Performs port scan on the target IP (tested on the local host) and provides the scan results. Implemented with sockets and nmap.

### Features:
Generates links to speedguide.com for any discovered ports for more information.
Vulnerability report based on different port scan scenarios. The scan returns stats for:</br>
1.Single vulnerable / non vulnerable port(s);</br>
2.Many vulnerable / non vulnerable ports all together;</br>
3.Either vulnerable or non vulnerable ports.</br>
4.Scan returns no ports or scan errors</br></br>

## Implementation of network discovery (completed)
Performs network discovery on the specified domain or network (tested on the local network only with dummy data).

### Features:
Performs the scan and provides connected hosts.
