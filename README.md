# Doodle-x-research-tool
Web app that visualizes and performs network scans. </br>I work on this project as a part of my constant learning about security and web development.</br></br>

## Implementation of traceroute

Performs traceroute and unloads detailed information with stats graphs using Charts.js</br>

## Features:
1.Processes the traceroute with detailed stats, including: country, city, region, country area, ISP/organization</br>
2.Builds different graphs and charts based on the traceroute results: ping, organization, type of IP adress.


## Implementation of port scan (completed)
Performs port scan on the target IP (tested on the local host) and provides the scan results.  Implemented with sockets. Nmap solution is also implemented, but works only from the console, you can run it within your enviroment as ``` python3 portscan_nmap.py ``` (Nmap scan conflicts with the Django instance).</br></br>

### Features:
Generates links to speedinfo.com for any discovered ports for more information.
Vulnerability report based on different port scan scenarios. The scan returns stats for:</br>
1.Single vulnerable / non vulnerable port(s);</br>
2.Many vulnerable / non vulnerable ports all together;</br>
3.Either vulnerable or non vulnerable ports.</br>
4.Scan returns no ports or scan errors</br></br>
