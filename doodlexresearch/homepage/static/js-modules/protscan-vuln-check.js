// Mapping the most vulnerable ports for the system 
// I created the list based on the different cyber security related articles
// The list could be expanded for different threats/needs of your projects

const vulnerable_ports = {

    15: `Port used by Netstat`,

    20: `Port used by FTP`,

    21: `Port used by FTP`,

    22: `Port used by SSH`,

    23: `Port used by Telnet`,

    25: `Port used by SMTP`,

    49: `Port used by Login Host Protocol`,

    50: `Port used by Remote Mail Checking Protocol`,

    51: `Port used by Terminal Access Controller Access-Control System`,

    53: `Port used by DNS`,

    67: `Port used by Bootstrap protocol server`,

    68: `Port used by Bootstrap protocol client`,

    69: `Port used by Trivial File Transfer Protocol`,

    79: `Port used by Finger - User Information Protocol`,

    80: `Port used by Hyper Text Transfer Protocol `,

    88: `Port used by Kerberos`,

    110: `Port used by POP3`,

    111: `Port used by SUN Remote Procedure Call`,

    119: `Port used by NNTP - Network News Transfer Protocol`,

    123: `Port used by NTP -  Network Time Protocol`,

    137: `Port used by NetBIOS - NETBIOS Name Service`,

    138: `Port used by NetBIOS - NETBIOS Datagram Service`,

    139: `Port used by NetBIOS - NETBIOS Session Service`,

    143: `Port used by IMAP - Internet Mail Access Protocol`,

    161: `Port used by SNMP - Simple network management protocol`,

    389: `Port used by LDAP - Lightweight Directory Access Protocol`,

    443: `Port used by HTTPS / SSL`,

    445: `Port used by SMB`,

    500: `Port used by ISAKMP - Internet Security Association and Key Management Protocol`,

    520: `Port used by RIP - Routing Information Protocol`,

    546: `Port used by DHCP`,

    547: `Port used by DHCP`,

    636: `Port used by LDAPS - Lightweight Directory Access Protocol over TLS/SSL`,

    1512: `Port used by Microsoft's Windows Internet Name Service`,

    1701: `Port used by L2TP`,

    1720: `Port used by H.323 Hostcall / multimedia apps`,

    1723: `Port used by PPTP VPN - Point-to-Point Tunneling Protocol Virtual Private Networking`,

    1812: `Port used by RADIUS - Authentication`,

    1813: `Port used by RAIUS - Accounting`,

    3389: `Port used by RDP - Remote Desktop`,

    5004: `Port used by RTP - Real-time Transport Protocol / media data `,

    5005: `Port used by RTP - Real-time Transport Protocol / control protocol `,

    5060: `Port used by SIP - Session Initiation Protocol`,

    5061: `port used by SIP-TLS - Session Initiation Protocol SIP over TLS`

}


export function generate_search_buttons_and_details(ports, mode) {
    
    // buttons for non vulnerable ports
    var buttons_s = ``;
    // buttons for vulnerable ports
    var buttons_w = ``;
    // vulnerable ports definition
    var details = ``;
    // combination of buttons and vulnerable port details 
    let row_info = ``;


    for (let i=0; i < ports.length; i++ ) {
        
        if ((typeof ports[i]) == "object") {

            if (mode="safe") {

                buttons_s += `<a class="btn btn-warning m-3" href="https://www.speedguide.net/port.php?port=${ports[i][0]}" target="_blank">Check port ${ports[i][0]} in db</a>`;

            }

            if (mode=="unsafe") {

                buttons_w = `<a class="btn btn-danger m-3" href="https://www.speedguide.net/port.php?port=${ports[i][0]}" target="_blank">Check port ${ports[i][0]} in db</a></br>`;
                details += `<p class="m-3 align-middle">${vulnerable_ports[ports[i][0]]}</p></br>`;

            }

        }

        else if ((typeof ports[i]) == "string") {

            if (mode=="safe") {

                buttons_s += `<a class="btn btn-warning m-3 text-center" href="https://www.speedguide.net/port.php?port=${ports[i]}" target="_blank">Check port ${ports[i]} in db</a>`;

            }

            if (mode=="unsafe") {

                buttons_w = `<a class="btn btn-danger m-3 text-center" href="https://www.speedguide.net/port.php?port=${ports[i]}" target="_blank">Check port ${ports[i]} in db</a>`;
                details = `<p class="m-3 p-auto text-center">${vulnerable_ports[ports[i]]}</p>`;
                row_info += 
                `<div class="container m-auto text-center">
                    <div class="row">
                        <div class="col">
                            ${details}
                        </div>
                                    
                        <div class="col">
                            ${buttons_w}
                        </div>
                    </div>
                </div>
                `;

            }

        }
    
    }

    if (mode=="unsafe"){

        return row_info
    }

    else {

        return buttons_s

    }

}

export function set_status_safe_single_port(port) {

    let message = `
    <div>
        <div class="vulnerability-result">
            <h3 class="vulnerability-title mx-auto text-center p-3">Vulnerability Report</h3>
            <p class="single-port-paragraph text-center">
                We were not able to locate port ${port} in the list of most targeted ports, but it might be a vulnerability.</br> 
                You can read more about vulnerabilities for this port on speedguru.com</br> 
                <a class="btn btn-warning m-3" href="https://www.speedguide.net/port.php?port=${port} target="_blank">Check port ${port} in db</a>
            </p>
        </div>
    </div>
    `;

    $('.portscan-results').append(message);
} 

export function set_status_unsafe_single_port(port, info) {
    let message = `
    <div>
        <div class="vulnerability-result">
            <h3 class="vulnerability-title mx-auto p-3 text-center">Vulnerability Report</h3>
            <div class="vulnerability-message">
                <p class="single-port-paragraph text-center">We identified that <b>port ${port}</b> is in the list of the most targeted ports. It's highly recommended that you close it or identify the user/process running.</br> You can learn more on this port and vulnerabilities on speedguide.com</p>

                <div class="row">
                    <div class="container m-auto text-center">
                        <div class="row">
                            <div class="col">
                                ${info}
                            </div>
                                        
                            <div class="col">
                                <a class="btn btn-danger" href="https://www.speedguide.net/port.php?port=${port} target="_blank">Check port ${port} in db</a>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    `;

    $('.portscan-results').append(message);
} 

export function set_status_safe_many_ports(ports) {
    
    let buttons = generate_search_buttons_and_details(ports, "safe");

    let message = `
    <div>
        <div class="vulnerability-result">
            <h3 class="vulnerability-title mx-auto text-center p-3">Vulnerability Report</h3>
                <p class="many-ports-paragraph text-center">
                    We were not able to locate discovered ports in the list of the most targeted ports, but they still might be a vulnerability.</br>
                    You can read more about these ports on speedguru.com</br>
                    ${buttons}
                </p>
        </div>
    </div>
    `;
    $('.portscan-results').append(message);

}

export function set_status_unsafe_many_ports(ports) {

    let result = generate_search_buttons_and_details(ports, "unsafe");

    let message = `
    <div>
        <div class="vulnerability-result">
            <h3 class="vulnerability-title mx-auto p-3 text-center">Vulnerability Report</h3>
            <div class="vulnerability-message">
                <p class="single-port-paragraph text-center">We identified that scanned ports are in the list of the most targeted ports. It's highly recommended that you close them or identify the user/process running. You can learn more on these ports and vulnerabilities on speedguide.com</p>

                <div class="row">
                    ${result}
                </div>
            </div>
        </div>
    </div>
    `;
    $('.portscan-results').append(message);


}

export function set_status_mixed_many_ports(ports) {

    let result = generate_search_buttons_and_details(ports, "safe");

    let message = `
    <div>
        <div class="vulnerability-result">
            <div class="vulnerability-message">
                <h3 class="vulnerability-title mx-auto m-3 p-3 text-center">Additional information</h3>
                <p class="single-port-paragraph text-center">The remaining ports are not in the list of the most targeted ones, but they still might be a vulnerability.</br>
                You can read more about these ports on speedguru.com</br></p>
                <div class="row">
                    ${result}
                </div>
            </div>
        </div>
    </div>
    `;
    $('.portscan-results').append(message);

}

export function set_status_no_ports() {
    let message = `
    <div>
        <div class="vulnerability-result">
            <h3 class="vulnerability-title mx-auto p-3 text-center">Vulnerability Report</h3>
            <div class="vulnerability-message">
                <p class="single-port-paragraph text-center">We were not able to locate open ports. Try providing different host name or make sure the firewall doesn't block the requests.</p>
            </div>
        </div>
    </div>
    `;
    $('.portscan-results').append(message);
}

export function check_if_ports_vulnerable(port_list){

    // Ports that are in the list of vulnerable ones
    var w_ports = [];

    // Ports that are not vulnerable
    var s_ports = [];

    var ports = Object.keys(vulnerable_ports);


    // Checking if single port/message
    if (port_list.length == 1) {

    // Checking if contains the port or just a message:
        // If port:
        if (parseInt(port_list[0][0]) >= 1) {
            
            var port = port_list[0][0];

            // If port is vulnerable
            if (ports.includes(port)) {

                // Passing the port --> str, corresponding value --> str
                set_status_unsafe_single_port(port, vulnerable_ports[port]);
            }

            // If not vulnerable
            else {

                set_status_safe_single_port(port);

            }
        }

        // If Message
        else {


            /// TODO: Implement the function with the template (no buttons)
            set_status_no_ports();

        }
    }

    // Guranteed that listed ports are open with no error message
    else if (port_list.length > 1) {

        for (let i=0; i < port_list.length; i++ ) {

            if (ports.includes((port_list[i][0]))) {

                w_ports.push(port_list[i][0]);

            }

            else {
                s_ports.push((port_list[i][0]));
            }
        }

        // If there are warning ports

        if (w_ports.length >= 1 && s_ports.length == 0) {

            set_status_unsafe_many_ports(w_ports);

        }
        
        else if (w_ports.length >= 1 && s_ports.length >= 1) {

            set_status_unsafe_many_ports(w_ports);
            set_status_mixed_many_ports(s_ports);

        }

        else {

            set_status_safe_many_ports(port_list);

        }

    }
}