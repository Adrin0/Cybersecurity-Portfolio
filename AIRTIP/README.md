# Incident Response Platform Project

This project involves setting up an incident response platform using Docker, VirtualBox, and Virtual Machines (VMs) to provide a comprehensive security monitoring and automation solution. The platform is configured with a SIEM (Security Information and Event Management) stack (ELK), threat intelligence, and automated response capabilities.

## Table of Contents
1. [Project Overview](#project-overview)
2. [Requirements](#requirements)
3. [Architecture](#architecture)
4. [Setup Instructions](#setup-instructions)
   - [VM Configuration](#vm-configuration)
   - [Network Configuration](#network-configuration)
   - [Environment Setup](#environment-setup)
5. [Platform Components](#platform-components)
   - [SIEM Stack (ELK)](#siem-stack-elk)
   - [Threat Intelligence Integration](#threat-intelligence-integration)
   - [Automation Scripts](#automation-scripts)
6. [Testing & Usage](#testing--usage)
7. [Future Enhancements](#future-enhancements)

---

## Project Overview

The Incident Response Platform is a lab environment designed for security monitoring, threat detection, and automated responses. This project is built using Docker containers and VirtualBox VMs to simulate an enterprise network environment, capturing logs, enriching them with threat intelligence, and responding to potential incidents.

## Requirements

- **Oracle VirtualBox** (for virtual machine management)
- **PowerShell** (for automated network and VM configuration)
- **Docker & Docker Compose** (for containerized services)
- **Ubuntu Server** for VMs
- **Kali Linux** for Vulnerable/Testing VM
- **Python** (for automation scripts)

## Architecture

The platform is organized into three primary VMs, each serving a specific purpose within the internal network.

| VM Name               | OS             | Role                                       |
|-----------------------|----------------|--------------------------------------------|
| **SIEM & Monitoring** | Ubuntu Server  | Hosts ELK Stack and Filebeat for log collection |
| **Threat Intel & Automation** | Ubuntu Server | Runs threat intel and automation scripts in Docker |
| **Vulnerable/Testing** | Kali Linux | Generates test logs and malicious activity |

### Network Setup

All VMs are connected to an internal network (`AIRTIP-Net`) configured with DHCP. This network is isolated to simulate a secure lab environment, and each VM is assigned a static IP for easy access between components.

## Setup Instructions

### VM Configuration
**Download VM Images**

- [Ubuntu Server](https://ubuntu.com/download/server)
- [Kali Linux](https://www.kali.org/get-kali/#kali-virtual-machines)

**For each VM, ensure the following hardware specifications:**
- **ELK-Server**: 4 Cores, 8gb RAM, 25gb Storage
- **Threat-Intel-Server**: 2 Cores, 4gb RAM, 25gb Storage
- **Kali VM**: 2 Cores, 2gb RAM, 25gb Storage
- **Network**: Internal network adapter set to `AIRTIP-Net` and NAT network adapter enabled


### Network Configuration

#### Step 1: Configure VMs for Internet Access

1. **Attach a NAT Network Adapter to each VM**
    - Open the VirtualBox settings for each VM.
    - Under the Network tab, ensure the first adapter is set to NAT for internet access.
2. **Power On and Update Each VM**
    - Start each VM and ensure it has internet connectivity.
    - Use the respective package manager to update the OS and install all required dependencies:
        - **ELK-Server**: Install Java, Elasticsearch, Logstash, and Kibana.
        - **Threat-Intel-Server**: Install Python and necessary threat intelligence tools.
        - **Kali VM**: Update all pentesting tools and utilities.
3. **Verify All Dependencies are installed before proceeding**

#### Step 2: Create and Configure an Internal Network

1. **Create an Internal Network in VirtualBox**
    - Open File > Host Network Manager in VirtualBox.
    - Configure the IP range (e.g., 192.168.56.1/24) and enable DHCP.
    - (Optional) Use PowerShell to configure DHCP:
    ```powershell
    VBoxManage dhcpserver add --network=AIRTIP-Net --server-ip=192.168.56.1 --lower-ip=192.168.56.2 --upper-ip=192.168.56.24 --netmask=255.255.255.0 --enable
    ```
2. **Assign Static IPs to each VM**
**IP Addresses**
- **ELK-Server**: 192.168.56.7
- **Threat-Intel-Server**: 192.168.56.8
- **Kali-VM**: 192.168.56.9

### Environment Setup

1. **Configure SSH on both Ubuntu Servers and Kali VM, then Login to each server**

   **Ubuntu**:
      - [Ubuntu Setup](docs/Ubuntu-Setup.md)

   **Kali/Ubuntu**:
      - [Kali SSH Setup](docs/Kali-SSH-Setup.md)
- On Kali machine, SSH into each server.
   ```bash
   ssh adrino@192.168.56.7
   ssh adrino@192.168.56.8
   ```

2. **Add Project Directories to each VM**
- **ELK-Server:**
```bash 
  mkdir -p /home/adrino/airtiplab/siem/{docker-configs, filebeat-configs, logs, sripts}
```
- **Threat-Intel-Server:**
```bash 
  mkdir -p ~/home/adrino/airtiplab/tis/{config, data, docker-configs, scripts}
```
- **Kali-VM:**
```bash 
  mkdir -p /home/kali/airtiplab/attacker{scripts, tools}
```
3. **Update System Packages on each VM** 
```bash 
  sudo apt-get update && sudo apt-get upgrade -y
```
4. **Fetch Installer Tools for each VM**
```bash
  sudo apt-get install -y python3 python3-pip curl wget git
```
5. **Install Docker and Docker Compose on Both Ubuntu Servers**
- **Install Docker**
   - Install docker command:
   ```bash
   sudo apt install docker.io -y
   sudo systemctl enable --now docker
   ```
- **Install Docker Compose**
   - command to install docker compose:
   ```bash
   sudo curl -L https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m) -o /usr/local/bin/docker-compose
   sudo chmod +x /usr/local/bin/docker-compose
   ```
- **Verify Installation**
   ```bash
   docker-compose --version
   ```
6. **Fetch and Install Dependencies**
- **ELK-Server**
  ```bash
  wget -O /home/adrino/airtiplab/siem/requirements-siem.txt https://your-source-url/requirements-siem.txt
  ```
- **Threat-Intel-Server**
  ```bash

  ```
## Platform Components

### SIEM Stack (ELK)

1. **Set Up ELK Stack**
   - Create a `docker-compose.yml` file for Elasticsearch, Logstash, and Kibana on the SIEM server.
   - Example `docker-compose.yml`:
     ```yaml
     version: '3.3'
     services:
       elasticsearch:
         image: docker.elastic.co/elasticsearch/elasticsearch:8.9.2
         container_name: elasticsearch
         environment:
           - discovery.type=single-node
         ulimits:
           memlock:
             soft: -1
             hard: -1
         ports:
           - "9200:9200"
           - "9300:9300"
         volumes:
           - es_data:/usr/share/elasticsearch/data
       kibana:
         image: docker.elastic.co/kibana/kibana:8.9.2
         container_name: kibana
         ports:
           - "5601:5601"
         environment:
           ELASTICSEARCH_HOSTS: http://elasticsearch:9200
         depends_on:
           - elasticsearch
     volumes:
       es_data:
     ```

2. **Launch the Stack**
   - Start the containers:
     ```bash
     sudo docker-compose up -d
     ```
   - Verify the services:
     - Elasticsearch: Visit `http://192.168.56.7:9200`
     - Kibana: Visit `http://192.168.56.7:5601`

3. **Integrate Filebeat**
   - Install Filebeat on the SIEM server:
     ```bash
     sudo apt update
     sudo apt install filebeat -y
     ```
   - Configure Filebeat to send logs to Logstash:
     - Edit `/etc/filebeat/filebeat.yml`:
       ```yaml
       output.logstash:
         hosts: ["192.168.56.7:5044"]
       ```
   - Start Filebeat:
     ```bash
     sudo systemctl enable filebeat
     sudo systemctl start filebeat
     ```

---

### Threat Intelligence Integration

1. **Install Python and Required Libraries**
   - Install Python3 and pip:
     ```bash
     sudo apt update
     sudo apt install python3 python3-pip -y
     ```
   - Install required libraries:
     ```bash
     pip3 install requests
     ```

2. **Set Up AbuseIPDB Integration**
   - Create a Python script (`abuseipdb.py`) to check logs for malicious IPs:
     ```python
     import requests

     API_KEY = "your_abuseipdb_api_key"
     LOG_FILE = "/var/log/syslog"

     def check_ip(ip):
         url = f"https://api.abuseipdb.com/api/v2/check"
         headers = {"Key": API_KEY, "Accept": "application/json"}
         params = {"ipAddress": ip, "maxAgeInDays": "90"}
         response = requests.get(url, headers=headers, params=params)
         return response.json()

     # Read IPs from log file
     with open(LOG_FILE, 'r') as file:
         for line in file:
             if "SRC=" in line:
                 ip = line.split("SRC=")[1].split()[0]
                 result = check_ip(ip)
                 print(f"IP: {ip} | Abuse Confidence: {result['data']['abuseConfidenceScore']}")
     ```

3. **Run the Script**
   - Execute the script:
     ```bash
     python3 abuseipdb.py
     ```

---

### Automation Scripts

1. **Create Incident Response Script**
   - Example script to block malicious IPs:
     ```python
     import os

     def block_ip(ip):
         os.system(f"sudo ufw deny from {ip}")
         print(f"Blocked IP: {ip}")

     # Example malicious IP list
     malicious_ips = ["192.168.1.100", "10.0.0.5"]

     for ip in malicious_ips:
         block_ip(ip)
     ```

2. **Integrate with ELK Logs**
   - Modify the script to parse Elasticsearch logs and block IPs dynamically:
     ```python
     import requests

     ELASTICSEARCH_URL = "http://192.168.56.7:9200"
     MALICIOUS_LOG_INDEX = "filebeat-*"

     def get_malicious_ips():
         response = requests.get(f"{ELASTICSEARCH_URL}/{MALICIOUS_LOG_INDEX}/_search", params={"q": "malicious:true"})
         return [hit["_source"]["ip"] for hit in response.json()["hits"]["hits"]]

     for ip in get_malicious_ips():
         block_ip(ip)
     ```

---

## Testing & Usage

1. **Simulate Attacks from Kali VM**
   - Perform the following actions:
     - Port scan using `nmap`:
       ```bash
       nmap -sS 192.168.56.7
       ```
     - Brute force SSH using `hydra`:
       ```bash
       hydra -l root -P /usr/share/wordlists/rockyou.txt ssh://192.168.56.7
       ```

2. **Verify Logs in ELK**
   - Open Kibana (`http://192.168.56.7:5601`) and check the logs dashboard for alerts related to the simulated attacks.

3. **Test Automation**
   - Run the incident response script and confirm malicious IPs are blocked on the SIEM server:
     ```bash
     sudo ufw status
     ```

---

## Future Enhancements

1. Add additional threat intelligence feeds like AlienVault OTX.
2. Implement automated email notifications for critical alerts.
3. Expand the lab environment to include Windows systems for endpoint monitoring.

---
