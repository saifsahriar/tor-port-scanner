# Tor Port Scanner

This project is a Python-based port scanner that uses the Tor network for anonymity. It scans a specified target for open ports, routing the traffic through Tor to mask the origin of the scan.

## Features

- Scans common ports through the Tor network
- Verifies Tor connection before scanning

## Prerequisites

- Python 3.6+
- Tor service installed and running on your system

## Installation

1. ```git clone https://github.com/saifsahriar/tor-port-scanner/```
2. ```cd tor-port-scanner```
3. ```pip install -r requirements.txt```

## Usage

1. Ensure Tor is running on your system:
- On most Linux systems: `sudo systemctl start tor`
- On macOS with Homebrew: `brew services start tor`

2. Run the scanner: ```python3 portscanner.py www.hackerone.com```
   
3. After use, you may want to stop the Tor service:
- On most Linux systems: `sudo systemctl stop tor`
- On macOS with Homebrew: `brew services stop tor`
