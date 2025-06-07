from flask import Flask, render_template, jsonify, request
import json
from datetime import datetime
import random
import time

app = Flask(__name__)

# Enhanced networking data with more comprehensive information
network_protocols = {
    "application_layer": [
        {"name": "HTTP/HTTPS", "port": "80/443", "purpose": "Web communication", "status": "active", "security": "TLS"},
        {"name": "FTP/SFTP", "port": "21/22", "purpose": "File transfer", "status": "active", "security": "SSH/TLS"},
        {"name": "SMTP", "port": "25/587/465", "purpose": "Email sending", "status": "active", "security": "TLS"},
        {"name": "POP3/IMAP", "port": "110/143", "purpose": "Email retrieval", "status": "active", "security": "TLS"},
        {"name": "DNS", "port": "53", "purpose": "Domain name resolution", "status": "critical", "security": "DNSSEC"},
        {"name": "DHCP", "port": "67/68", "purpose": "IP address assignment", "status": "active",
         "security": "Authentication"},
        {"name": "SSH", "port": "22", "purpose": "Secure remote access", "status": "active", "security": "Encryption"},
        {"name": "Telnet", "port": "23", "purpose": "Remote terminal", "status": "legacy", "security": "None"},
        {"name": "SNMP", "port": "161/162", "purpose": "Network management", "status": "active", "security": "SNMPv3"},
        {"name": "NTP", "port": "123", "purpose": "Time synchronization", "status": "critical",
         "security": "Authentication"}
    ],
    "transport_layer": [
        {"name": "TCP", "purpose": "Reliable connection-oriented",
         "features": ["Flow control", "Error recovery", "Ordering", "Congestion control"]},
        {"name": "UDP", "purpose": "Fast connectionless",
         "features": ["Low latency", "Real-time", "Broadcasting", "Multicast"]},
        {"name": "SCTP", "purpose": "Advanced transport",
         "features": ["Multi-homing", "Multi-streaming", "Reliability", "Message-oriented"]},
        {"name": "QUIC", "purpose": "Modern web transport",
         "features": ["HTTP/3", "Built-in encryption", "Multiplexing", "0-RTT"]}
    ],
    "network_layer": [
        {"name": "IPv4", "addresses": "4.3 billion", "format": "xxx.xxx.xxx.xxx", "status": "exhausted",
         "adoption": "95%"},
        {"name": "IPv6", "addresses": "340 undecillion", "format": "xxxx:xxxx:xxxx:xxxx", "status": "growing",
         "adoption": "38%"},
        {"name": "ICMP", "purpose": "Error reporting", "tools": ["ping", "traceroute"], "status": "essential"},
        {"name": "ARP", "purpose": "Address resolution", "scope": "local network", "status": "fundamental"},
        {"name": "BGP", "purpose": "Internet routing", "scope": "global", "status": "critical", "routes": "930K+"},
        {"name": "OSPF", "purpose": "Internal routing", "scope": "enterprise", "status": "standard"}
    ]
}

security_topics = [
    {"name": "Next-Gen Firewalls", "type": "Perimeter Defense",
     "technologies": ["Deep packet inspection", "Application control", "Threat intelligence", "SSL inspection"]},
    {"name": "Zero Trust VPN", "type": "Secure Access",
     "technologies": ["WireGuard", "OpenVPN", "IPSec", "Zero Trust Network Access"]},
    {"name": "AI-Powered IDS/IPS", "type": "Threat Detection",
     "technologies": ["Machine learning", "Behavioral analysis", "Threat hunting", "Real-time response"]},
    {"name": "Micro-Segmentation", "type": "Network Isolation",
     "technologies": ["Software-defined perimeters", "Identity-based access", "Least privilege", "Dynamic policies"]},
    {"name": "Advanced DDoS Protection", "type": "Availability",
     "technologies": ["Cloud scrubbing", "Rate limiting", "Behavioral analysis", "Automated mitigation"]},
    {"name": "Quantum-Safe Encryption", "type": "Future Security",
     "technologies": ["Post-quantum cryptography", "Quantum key distribution", "Lattice-based crypto",
                      "Future-proof algorithms"]}
]

modern_technologies = [
    {"name": "5G/6G Networks", "category": "Mobile",
     "features": ["Ultra-low latency (<1ms)", "Massive IoT (1M devices/km²)", "Network slicing", "Edge integration"]},
    {"name": "Intent-Based SD-WAN", "category": "Enterprise",
     "features": ["AI-driven optimization", "Zero-touch provisioning", "Multi-cloud connectivity",
                  "Policy automation"]},
    {"name": "Edge Computing", "category": "Infrastructure",
     "features": ["Real-time processing", "Local AI inference", "Reduced bandwidth", "5G integration"]},
    {"name": "Cloud-Native Networking", "category": "Virtualization",
     "features": ["Container networking", "Service mesh", "Kubernetes CNI", "Serverless networking"]},
    {"name": "AI/ML Network Operations", "category": "Intelligence",
     "features": ["Predictive maintenance", "Self-healing networks", "Anomaly detection", "Automated optimization"]},
    {"name": "Quantum Internet", "category": "Emerging",
     "features": ["Quantum entanglement", "Unhackable communication", "Quantum computing", "Research networks"]}
]

network_tools = [
    {"name": "Wireshark", "category": "Packet Analysis",
     "use_case": "Deep packet inspection with 3000+ protocol decoders and real-time capture"},
    {"name": "Nmap", "category": "Network Discovery",
     "use_case": "Advanced port scanning, OS detection, and network mapping with NSE scripting"},
    {"name": "ping", "category": "Connectivity",
     "use_case": "Basic reachability testing and round-trip time measurement"},
    {"name": "traceroute", "category": "Path Analysis",
     "use_case": "Network path discovery, latency measurement, and hop identification"},
    {"name": "iperf3", "category": "Performance",
     "use_case": "Comprehensive bandwidth testing with multi-threading and JSON output"},
    {"name": "tcpdump", "category": "Packet Capture",
     "use_case": "Command-line packet analysis with powerful filtering capabilities"},
    {"name": "Netstat", "category": "Connection Monitoring",
     "use_case": "Active connection monitoring and network statistics"},
    {"name": "Prometheus + Grafana", "category": "Monitoring",
     "use_case": "Enterprise-grade monitoring with time-series data and visualization"}
]

cloud_networking = {
    "aws": ["VPC", "ELB", "CloudFront", "Route 53", "Direct Connect", "Transit Gateway", "AWS Global Accelerator"],
    "azure": ["Virtual Network", "Load Balancer", "CDN", "DNS", "ExpressRoute", "Virtual WAN", "Front Door"],
    "gcp": ["VPC", "Cloud Load Balancing", "Cloud CDN", "Cloud DNS", "Cloud Interconnect",
            "Network Intelligence Center"],
    "concepts": ["Software-Defined Networking", "Micro-segmentation", "Service Mesh", "Container Networking",
                 "Multi-cloud", "Hybrid Cloud"]
}

performance_metrics = {
    "bandwidth": {"unit": "bps", "description": "Maximum data transfer capacity", "optimal": "> 100 Mbps"},
    "latency": {"unit": "ms", "description": "Round-trip time delay", "optimal": "< 20 ms"},
    "jitter": {"unit": "ms", "description": "Latency variation", "optimal": "< 5 ms"},
    "packet_loss": {"unit": "%", "description": "Lost packet percentage", "optimal": "< 0.1%"},
    "throughput": {"unit": "bps", "description": "Actual data transfer rate", "optimal": "> 80% of bandwidth"},
    "mtu": {"unit": "bytes", "description": "Maximum transmission unit", "optimal": "1500 bytes (Ethernet)"}
}


# Enhanced route handlers
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


# Enhanced API endpoints with more realistic data
@app.route('/api/network-stats')
def api_network_stats():
    """Enhanced global network statistics with trends"""
    base_time = time.time()
    stats = {
        "global_traffic": f"{random.uniform(4.5, 5.8):.1f} ZB/month",
        "internet_users": f"{random.uniform(5.1, 5.4):.2f} billion",
        "connected_devices": f"{random.randint(48, 55)} billion",
        "data_centers": f"{random.randint(8, 12)} million",
        "submarine_cables": f"{random.randint(420, 460)}",
        "bgp_routes": f"{random.randint(920, 960)}K",
        "dns_queries": f"{random.randint(4, 7)} trillion/day",
        "ddos_attacks": f"{random.randint(15, 35)}/minute",
        "ipv6_adoption": f"{random.uniform(35, 42):.1f}%",
        "ssl_traffic": f"{random.uniform(85, 92):.1f}%",
        "timestamp": datetime.now().isoformat(),
        "trend_data": {
            "traffic_growth": f"+{random.uniform(15, 25):.1f}% YoY",
            "device_growth": f"+{random.uniform(8, 15):.1f}% YoY",
            "security_incidents": f"+{random.uniform(20, 35):.1f}% YoY"
        }
    }
    return jsonify(stats)


@app.route('/api/protocol-usage')
def api_protocol_usage():
    """Real-time protocol usage with detailed metrics"""
    usage = {
        "http_https": {"percentage": random.randint(75, 85), "trend": "increasing"},
        "tcp": {"percentage": random.randint(85, 95), "trend": "stable"},
        "udp": {"percentage": random.randint(65, 75), "trend": "increasing"},
        "ipv4": {"percentage": random.randint(92, 98), "trend": "decreasing"},
        "ipv6": {"percentage": random.randint(35, 45), "trend": "increasing"},
        "dns": {"percentage": random.randint(99, 100), "trend": "stable"},
        "tls": {"percentage": random.randint(80, 90), "trend": "increasing"},
        "quic": {"percentage": random.randint(15, 25), "trend": "rapidly_increasing"},
        "http3": {"percentage": random.randint(8, 18), "trend": "rapidly_increasing"}
    }
    return jsonify(usage)


@app.route('/api/security-threats')
def api_security_threats():
    """Enhanced security threat landscape with detailed metrics"""
    threats = {
        "malware_families": random.randint(1200, 1800),
        "phishing_sites": random.randint(50, 150),
        "botnets_active": random.randint(15, 35),
        "zero_days": random.randint(20, 40),
        "ransomware_variants": random.randint(150, 250),
        "threat_level": random.choice(["LOW", "MODERATE", "HIGH", "CRITICAL"]),
        "threat_categories": {
            "malware": f"{random.randint(35, 45)}%",
            "phishing": f"{random.randint(25, 35)}%",
            "ddos": f"{random.randint(15, 25)}%",
            "data_breach": f"{random.randint(10, 20)}%",
            "insider_threat": f"{random.randint(5, 15)}%"
        },
        "geographic_distribution": {
            "asia_pacific": f"{random.randint(35, 45)}%",
            "north_america": f"{random.randint(25, 35)}%",
            "europe": f"{random.randint(20, 30)}%",
            "other": f"{random.randint(5, 15)}%"
        }
    }
    return jsonify(threats)


@app.route('/api/performance-test')
def api_performance_test():
    """Comprehensive network performance test simulation"""
    test_result = {
        "download_speed": f"{random.uniform(50, 1000):.1f} Mbps",
        "upload_speed": f"{random.uniform(10, 500):.1f} Mbps",
        "latency": f"{random.randint(8, 50)} ms",
        "jitter": f"{random.uniform(1, 10):.1f} ms",
        "packet_loss": f"{random.uniform(0, 2):.3f}%",
        "server_location": random.choice(["New York", "London", "Tokyo", "Sydney", "Frankfurt"]),
        "connection_type": random.choice(["Fiber", "Cable", "DSL", "5G", "Satellite"]),
        "quality_score": random.randint(60, 100),
        "recommendations": [
            "Consider upgrading to fiber for better performance",
            "Check for network congestion during peak hours",
            "Optimize router placement for better WiFi coverage"
        ]
    }
    return jsonify(test_result)


@app.route('/api/trace-route')
def api_trace_route():
    """Enhanced traceroute simulation with realistic network topology"""
    hops = []
    base_latency = random.uniform(1, 3)
    destinations = [
        "192.168.1.1 (Home Router)",
        "10.0.0.1 (ISP Gateway)",
        "172.16.1.1 (Regional Hub)",
        "203.0.113.1 (Tier 1 Backbone)",
        "198.51.100.1 (CDN Edge)",
        "8.8.8.8 (Google DNS)"
    ]

    for i, dest in enumerate(destinations):
        base_latency += random.uniform(3, 15)
        success_rate = random.uniform(95, 100) if i < 4 else random.uniform(98, 100)
        hops.append({
            "hop": i + 1,
            "destination": dest,
            "latency": f"{base_latency:.1f} ms",
            "success_rate": f"{success_rate:.1f}%",
            "status": "success" if success_rate > 90 else "timeout"
        })

    return jsonify({
        "hops": hops,
        "total_hops": len(hops),
        "total_time": f"{base_latency:.1f} ms",
        "path_quality": "Good" if all(h["status"] == "success" for h in hops) else "Degraded"
    })


@app.route('/api/network-topology')
def api_network_topology():
    """Enhanced network topology with realistic infrastructure"""
    topology = {
        "nodes": [
            {"id": "internet", "type": "cloud", "label": "Internet", "status": "active"},
            {"id": "firewall", "type": "security", "label": "Next-Gen Firewall", "status": "active"},
            {"id": "router", "type": "router", "label": "Core Router", "status": "active"},
            {"id": "switch1", "type": "switch", "label": "Access Switch A", "status": "active"},
            {"id": "switch2", "type": "switch", "label": "Access Switch B", "status": "active"},
            {"id": "server", "type": "server", "label": "Web Server", "status": "active"},
            {"id": "db", "type": "database", "label": "Database Server", "status": "active"},
            {"id": "wifi", "type": "wireless", "label": "WiFi Access Point", "status": "active"}
        ],
        "links": [
            {"source": "internet", "target": "firewall", "bandwidth": "10 Gbps", "utilization": "45%"},
            {"source": "firewall", "target": "router", "bandwidth": "10 Gbps", "utilization": "38%"},
            {"source": "router", "target": "switch1", "bandwidth": "1 Gbps", "utilization": "62%"},
            {"source": "router", "target": "switch2", "bandwidth": "1 Gbps", "utilization": "55%"},
            {"source": "switch1", "target": "server", "bandwidth": "1 Gbps", "utilization": "40%"},
            {"source": "switch2", "target": "db", "bandwidth": "1 Gbps", "utilization": "30%"},
            {"source": "switch1", "target": "wifi", "bandwidth": "1 Gbps", "utilization": "25%"}
        ]
    }
    return jsonify(topology)


@app.route('/api/bandwidth-calculator')
def api_bandwidth_calculator():
    """Enhanced bandwidth calculation with recommendations"""
    users = int(request.args.get('users', 100))
    app_type = request.args.get('app_type', 'office')

    bandwidth_per_user = {
        'office': 2,
        'video': 5,
        'streaming': 8,
        'design': 15,
        'development': 10,
        'cloud': 12
    }

    base_requirement = users * bandwidth_per_user.get(app_type, 2)
    peak_factor = random.uniform(1.3, 1.8)
    recommended = base_requirement * peak_factor * 1.2  # 20% buffer

    result = {
        "base_requirement": f"{base_requirement} Mbps",
        "peak_requirement": f"{base_requirement * peak_factor:.0f} Mbps",
        "recommended_bandwidth": f"{recommended:.0f} Mbps",
        "monthly_cost_estimate": f"${recommended * 2.5:.0f}",
        "recommendations": [
            "Consider redundant connections for critical applications",
            "Implement QoS policies for priority traffic",
            "Monitor usage patterns for optimization opportunities"
        ]
    }
    return jsonify(result)


@app.route('/api/network-health')
def api_network_health():
    """Comprehensive network health metrics"""
    health_data = {
        "overall_status": random.choice(["healthy", "warning", "critical"]),
        "uptime": f"{random.uniform(99.5, 99.99):.3f}%",
        "response_time": f"{random.randint(5, 25)} ms",
        "throughput": f"{random.randint(800, 1200)} Mbps",
        "error_rate": f"{random.uniform(0.01, 0.5):.3f}%",
        "active_connections": random.randint(500, 3000),
        "cpu_usage": f"{random.randint(15, 85)}%",
        "memory_usage": f"{random.randint(40, 90)}%",
        "disk_usage": f"{random.randint(30, 80)}%",
        "services": {
            "dns": random.choice(["healthy", "warning"]),
            "dhcp": "healthy",
            "web_server": random.choice(["healthy", "warning"]),
            "database": "healthy",
            "firewall": "healthy"
        },
        "alerts": [
            {"severity": "warning", "message": "High bandwidth usage detected", "time": "2 minutes ago"},
            {"severity": "info", "message": "Scheduled maintenance completed", "time": "1 hour ago"}
        ]
    }
    return jsonify(health_data)


if __name__ == '__main__':
    print("🌐 Starting tcp-ip.ch - The Ultimate TCP/IP Learning Platform")
    print("📚 Comprehensive networking education at your fingertips")
    print("🚀 Access your platform at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)