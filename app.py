from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime
import random

app = Flask(__name__)

# Comprehensive networking data
network_protocols = {
    "application_layer": [
        {"name": "HTTP/HTTPS", "port": "80/443", "purpose": "Web communication", "status": "active"},
        {"name": "FTP/SFTP", "port": "21/22", "purpose": "File transfer", "status": "active"},
        {"name": "SMTP", "port": "25", "purpose": "Email sending", "status": "active"},
        {"name": "POP3/IMAP", "port": "110/143", "purpose": "Email retrieval", "status": "active"},
        {"name": "DNS", "port": "53", "purpose": "Domain name resolution", "status": "active"},
        {"name": "DHCP", "port": "67/68", "purpose": "IP address assignment", "status": "active"},
        {"name": "SSH", "port": "22", "purpose": "Secure remote access", "status": "active"},
        {"name": "Telnet", "port": "23", "purpose": "Remote terminal", "status": "legacy"},
        {"name": "SNMP", "port": "161", "purpose": "Network management", "status": "active"},
        {"name": "NTP", "port": "123", "purpose": "Time synchronization", "status": "active"}
    ],
    "transport_layer": [
        {"name": "TCP", "purpose": "Reliable connection-oriented",
         "features": ["Flow control", "Error recovery", "Ordering"]},
        {"name": "UDP", "purpose": "Fast connectionless", "features": ["Low latency", "Real-time", "Broadcasting"]},
        {"name": "SCTP", "purpose": "Advanced transport",
         "features": ["Multi-homing", "Multi-streaming", "Reliability"]},
        {"name": "QUIC", "purpose": "Modern web transport", "features": ["HTTP/3", "Encryption", "Multiplexing"]}
    ],
    "network_layer": [
        {"name": "IPv4", "addresses": "4.3 billion", "format": "xxx.xxx.xxx.xxx", "status": "exhausted"},
        {"name": "IPv6", "addresses": "340 undecillion", "format": "xxxx:xxxx:xxxx:xxxx", "status": "growing"},
        {"name": "ICMP", "purpose": "Error reporting", "tools": ["ping", "traceroute"], "status": "essential"},
        {"name": "ARP", "purpose": "Address resolution", "scope": "local network", "status": "fundamental"},
        {"name": "BGP", "purpose": "Internet routing", "scope": "global", "status": "critical"},
        {"name": "OSPF", "purpose": "Internal routing", "scope": "enterprise", "status": "standard"}
    ]
}

security_topics = [
    {"name": "Firewalls", "type": "Perimeter Defense",
     "technologies": ["Packet filtering", "Stateful inspection", "Application layer"]},
    {"name": "VPN", "type": "Secure Tunneling", "technologies": ["IPSec", "OpenVPN", "WireGuard"]},
    {"name": "IDS/IPS", "type": "Threat Detection",
     "technologies": ["Signature-based", "Anomaly detection", "Behavioral analysis"]},
    {"name": "Network Segmentation", "type": "Access Control", "technologies": ["VLANs", "Subnetting", "Zero Trust"]},
    {"name": "DDoS Protection", "type": "Availability",
     "technologies": ["Rate limiting", "Traffic analysis", "Mitigation"]},
    {"name": "Network Encryption", "type": "Data Protection", "technologies": ["TLS/SSL", "IPSec", "End-to-end"]}
]

modern_technologies = [
    {"name": "5G Networks", "category": "Mobile", "features": ["Ultra-low latency", "Massive IoT", "Network slicing"]},
    {"name": "SD-WAN", "category": "Enterprise",
     "features": ["Centralized control", "Policy automation", "Cloud integration"]},
    {"name": "Edge Computing", "category": "Infrastructure",
     "features": ["Distributed processing", "Reduced latency", "Local data"]},
    {"name": "Network Function Virtualization", "category": "Virtualization",
     "features": ["Software-defined", "Scalability", "Flexibility"]},
    {"name": "Intent-Based Networking", "category": "AI/ML",
     "features": ["Self-configuring", "Policy automation", "Predictive analysis"]},
    {"name": "Quantum Networking", "category": "Emerging",
     "features": ["Quantum entanglement", "Ultra-secure", "Future internet"]}
]

network_tools = [
    {"name": "Wireshark", "category": "Packet Analysis",
     "use_case": "Deep packet inspection and network troubleshooting"},
    {"name": "Nmap", "category": "Network Discovery", "use_case": "Port scanning and network mapping"},
    {"name": "ping", "category": "Connectivity", "use_case": "Basic reachability testing"},
    {"name": "traceroute", "category": "Path Analysis", "use_case": "Network path discovery and latency measurement"},
    {"name": "iperf3", "category": "Performance", "use_case": "Bandwidth and throughput testing"},
    {"name": "tcpdump", "category": "Packet Capture", "use_case": "Command-line packet analysis"},
    {"name": "Netstat", "category": "Connection Monitoring", "use_case": "Active connection and port monitoring"},
    {"name": "PRTG", "category": "Network Monitoring", "use_case": "Enterprise network performance monitoring"}
]

cloud_networking = {
    "aws": ["VPC", "ELB", "CloudFront", "Route 53", "Direct Connect"],
    "azure": ["Virtual Network", "Load Balancer", "CDN", "DNS", "ExpressRoute"],
    "gcp": ["VPC", "Cloud Load Balancing", "Cloud CDN", "Cloud DNS", "Cloud Interconnect"],
    "concepts": ["Software-Defined Networking", "Micro-segmentation", "Service Mesh", "Container Networking"]
}

performance_metrics = {
    "bandwidth": {"unit": "bps", "description": "Data transfer capacity"},
    "latency": {"unit": "ms", "description": "Round-trip time delay"},
    "jitter": {"unit": "ms", "description": "Latency variation"},
    "packet_loss": {"unit": "%", "description": "Lost packet percentage"},
    "throughput": {"unit": "bps", "description": "Actual data transfer rate"},
    "mtu": {"unit": "bytes", "description": "Maximum transmission unit"}
}


# Routes
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/protocols')
def protocols():
    return render_template('protocols.html', protocols=network_protocols)


@app.route('/security')
def security():
    return render_template('security.html', security_topics=security_topics)


@app.route('/modern-tech')
def modern_tech():
    return render_template('modern_tech.html', technologies=modern_technologies)


@app.route('/tools')
def tools():
    return render_template('tools.html', tools=network_tools)


@app.route('/cloud')
def cloud():
    return render_template('cloud.html', cloud_data=cloud_networking)


@app.route('/performance')
def performance():
    return render_template('performance.html', metrics=performance_metrics)


@app.route('/osi-model')
def osi_model():
    return render_template('osi_model.html')


@app.route('/troubleshooting')
def troubleshooting():
    return render_template('troubleshooting.html')


@app.route('/future')
def future():
    return render_template('future.html')


# API Routes
@app.route('/api/network-stats')
def api_network_stats():
    # Simulate real-time network statistics
    stats = {
        "global_traffic": f"{random.uniform(4.5, 5.2):.1f} ZB/month",
        "internet_users": f"{random.uniform(5.1, 5.3):.2f} billion",
        "connected_devices": f"{random.randint(48, 52)} billion",
        "data_centers": f"{random.randint(8, 12)} million",
        "submarine_cables": f"{random.randint(420, 450)}",
        "bgp_routes": f"{random.randint(920, 950)}K",
        "dns_queries": f"{random.randint(4, 6)} trillion/day",
        "ddos_attacks": f"{random.randint(15, 25)}/minute"
    }
    return jsonify(stats)


@app.route('/api/protocol-usage')
def api_protocol_usage():
    # Simulate protocol usage statistics
    usage = {
        "http_https": random.randint(75, 85),
        "tcp": random.randint(85, 95),
        "udp": random.randint(65, 75),
        "ipv4": random.randint(92, 98),
        "ipv6": random.randint(35, 45),
        "dns": random.randint(99, 100),
        "tls": random.randint(80, 90)
    }
    return jsonify(usage)


@app.route('/api/security-threats')
def api_security_threats():
    # Simulate current security threat landscape
    threats = {
        "malware_families": random.randint(800, 1200),
        "phishing_sites": random.randint(50, 100),
        "botnets_active": random.randint(10, 25),
        "zero_days": random.randint(15, 30),
        "ransomware_variants": random.randint(100, 200),
        "threat_level": "MODERATE"
    }
    return jsonify(threats)


@app.route('/api/performance-test')
def api_performance_test():
    # Simulate network performance test
    test_result = {
        "download_speed": f"{random.uniform(50, 1000):.1f} Mbps",
        "upload_speed": f"{random.uniform(10, 100):.1f} Mbps",
        "latency": f"{random.randint(10, 50)} ms",
        "jitter": f"{random.randint(1, 10)} ms",
        "packet_loss": f"{random.uniform(0, 2):.2f}%",
        "server_location": "Global CDN"
    }
    return jsonify(test_result)


@app.route('/api/trace-route')
def api_trace_route():
    # Simulate traceroute to a destination
    hops = []
    base_latency = 1
    destinations = [
        "192.168.1.1 (Gateway)",
        "10.0.0.1 (ISP Router)",
        "172.16.1.1 (Regional Hub)",
        "203.0.113.1 (Backbone)",
        "198.51.100.1 (Peer Network)",
        "8.8.8.8 (Google DNS)"
    ]

    for i, dest in enumerate(destinations):
        base_latency += random.randint(5, 20)
        hops.append({
            "hop": i + 1,
            "destination": dest,
            "latency": f"{base_latency} ms",
            "status": "success"
        })

    return jsonify({"hops": hops, "total_hops": len(hops)})


@app.route('/api/network-topology')
def api_network_topology():
    # Simulate network topology data
    topology = {
        "nodes": [
            {"id": "internet", "type": "cloud", "label": "Internet"},
            {"id": "firewall", "type": "security", "label": "Firewall"},
            {"id": "router", "type": "router", "label": "Core Router"},
            {"id": "switch1", "type": "switch", "label": "Switch A"},
            {"id": "switch2", "type": "switch", "label": "Switch B"},
            {"id": "server", "type": "server", "label": "Web Server"},
            {"id": "db", "type": "database", "label": "Database"}
        ],
        "links": [
            {"source": "internet", "target": "firewall"},
            {"source": "firewall", "target": "router"},
            {"source": "router", "target": "switch1"},
            {"source": "router", "target": "switch2"},
            {"source": "switch1", "target": "server"},
            {"source": "switch2", "target": "db"}
        ]
    }
    return jsonify(topology)


@app.route('/api/bandwidth-test')
def api_bandwidth_test():
    # Simulate bandwidth test results
    test_result = {
        "download_speed": f"{random.uniform(100, 1000):.0f} Mbps",
        "upload_speed": f"{random.uniform(50, 500):.0f} Mbps",
        "latency": f"{random.randint(8, 50)} ms",
        "jitter": f"{random.uniform(1, 10):.1f} ms",
        "packet_loss": f"{random.uniform(0, 2):.3f}%",
        "test_server": "Global CDN",
        "timestamp": datetime.now().isoformat()
    }
    return jsonify(test_result)


@app.route('/api/network-health')
def api_network_health():
    # Simulate network health metrics
    health_data = {
        "overall_status": "healthy",
        "uptime": f"{random.uniform(99.5, 99.99):.2f}%",
        "response_time": f"{random.randint(10, 30)} ms",
        "throughput": f"{random.randint(800, 1200)} Mbps",
        "error_rate": f"{random.uniform(0.01, 0.1):.3f}%",
        "active_connections": random.randint(500, 2000),
        "cpu_usage": f"{random.randint(20, 80)}%",
        "memory_usage": f"{random.randint(40, 90)}%",
        "disk_usage": f"{random.randint(30, 70)}%"
    }
    return jsonify(health_data)


@app.route('/api/traffic-analysis')
def api_traffic_analysis():
    # Simulate traffic analysis data
    traffic_data = {
        "total_traffic": f"{random.uniform(500, 1500):.1f} GB/day",
        "peak_hour": "14:00-15:00",
        "top_protocols": [
            {"protocol": "HTTP/HTTPS", "percentage": random.randint(65, 85)},
            {"protocol": "TCP", "percentage": random.randint(10, 20)},
            {"protocol": "UDP", "percentage": random.randint(5, 15)},
            {"protocol": "ICMP", "percentage": random.randint(1, 5)}
        ],
        "geographic_distribution": [
            {"region": "North America", "percentage": random.randint(40, 60)},
            {"region": "Europe", "percentage": random.randint(20, 35)},
            {"region": "Asia", "percentage": random.randint(15, 25)},
            {"region": "Other", "percentage": random.randint(5, 15)}
        ],
        "bandwidth_utilization": {
            "current": f"{random.randint(40, 80)}%",
            "average": f"{random.randint(50, 70)}%",
            "peak": f"{random.randint(80, 95)}%"
        }
    }
    return jsonify(traffic_data)


@app.route('/api/device-inventory')
def api_device_inventory():
    # Simulate network device inventory
    devices = {
        "total_devices": random.randint(150, 300),
        "device_types": [
            {"type": "Workstations", "count": random.randint(80, 150), "status": "online"},
            {"type": "Servers", "count": random.randint(10, 25), "status": "online"},
            {"type": "Network Equipment", "count": random.randint(15, 30), "status": "online"},
            {"type": "Mobile Devices", "count": random.randint(50, 100), "status": "online"},
            {"type": "IoT Devices", "count": random.randint(20, 50), "status": "mixed"}
        ],
        "operating_systems": [
            {"os": "Windows", "percentage": random.randint(60, 80)},
            {"os": "macOS", "percentage": random.randint(15, 25)},
            {"os": "Linux", "percentage": random.randint(5, 15)},
            {"os": "Mobile OS", "percentage": random.randint(10, 20)}
        ],
        "last_updated": datetime.now().isoformat()
    }
    return jsonify(devices)


@app.route('/api/alerts')
def api_alerts():
    # Simulate network alerts
    alert_types = [
        {"type": "High Bandwidth Usage", "severity": "warning", "count": random.randint(1, 5)},
        {"type": "Device Offline", "severity": "critical", "count": random.randint(0, 3)},
        {"type": "Security Threat", "severity": "high", "count": random.randint(0, 2)},
        {"type": "Configuration Change", "severity": "info", "count": random.randint(2, 10)},
        {"type": "Performance Degradation", "severity": "warning", "count": random.randint(1, 4)}
    ]

    alerts = {
        "total_alerts": sum(alert["count"] for alert in alert_types),
        "alert_types": alert_types,
        "recent_alerts": [
            {
                "timestamp": (datetime.now().replace(minute=random.randint(0, 59))).isoformat(),
                "type": random.choice(["Bandwidth", "Security", "Performance", "Device"]),
                "message": f"Alert message {random.randint(1, 100)}",
                "severity": random.choice(["info", "warning", "high", "critical"])
            } for _ in range(5)
        ]
    }
    return jsonify(alerts)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)