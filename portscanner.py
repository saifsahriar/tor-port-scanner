#!/usr/bin/env python3
import sys
import socket
from termcolor import colored
import socks
import requests
from stem import Signal
from stem.control import Controller

top_ports = [
    20, 21, 22, 23, 25, 53, 80, 110, 111, 135, 139, 143, 443, 445, 993, 995,
    1723, 3306, 3389, 5900, 8080
]

def connect_to_tor():
    try:
        socks.set_default_proxy(socks.SOCKS5, "localhost", 9050)
        socket.socket = socks.socksocket
        print("[+] SOCKS proxy set")
    except Exception as e:
        print(colored(f"[!] Error setting SOCKS proxy: {e}", "yellow"))
        sys.exit(1)

def check_tor():
    try:
        session = requests.session()
        session.proxies = {'http':  'socks5h://localhost:9050',
                           'https': 'socks5h://localhost:9050'}
        r = session.get('https://check.torproject.org/')
        if 'Congratulations' in r.text:
            print("[+] Successfully connected to Tor")
            return True
        else:
            print(colored("[!] Connected to the proxy, but not using Tor", "yellow"))
            return False
    except requests.exceptions.RequestException as e:
        print(colored(f"[!] Error checking Tor connection: {e}", "yellow"))
        return False

'''
def renew_tor_ip():
    try:
        with Controller.from_port(port=9051) as controller:
            controller.authenticate()
            controller.signal(Signal.NEWNYM)
        print("[+] Tor IP renewed")
    except Exception as e:
        print(colored(f"[!] Error renewing Tor IP: {e}", "yellow"))
'''

def scan(target):
    try:
        ip_addr = socket.gethostbyname(target)
        print(f"[+] Resolved {target} to {ip_addr}")
    except socket.gaierror:
        print(colored(f"[!] Could not resolve hostname: {target}", "yellow"))
        return
    print()
    for port in top_ports:
        scan_ports(ip_addr, port)

def scan_ports(ip_addr, port):
    try:
        sock = socket.socket()
        sock.settimeout(3)
        result = sock.connect_ex((ip_addr, port))
        if result == 0:
            print(colored(f"[+] Open {port}", 'green'))
        else:
            print(colored(f"[-] Closed {port}", 'red'))
        sock.close()
    except socket.timeout:
        print(colored(f"[-] Closed {port}", 'red'))
    except socket.error as e:
        print(colored(f"[!] Error scanning {port}: {e}", 'yellow'))

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print("[+] Usage: python3 portscanner.py <www.website.com>")
        sys.exit(1)

    target = sys.argv[1]
    print("[+] Connecting to Tor...")
    connect_to_tor()
    
    if not check_tor():
        print(colored("[!] Not connected to Tor network", "yellow"))
        sys.exit(1)

#    renew_tor_ip()
    print("[+] Starting scan...")
    scan(target)
