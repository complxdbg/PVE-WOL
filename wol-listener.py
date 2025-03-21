#!/usr/bin/env python3

import socket
import os
import re
import subprocess
from datetime import datetime  # Importing datetime for timestamp

# Function to find VM/LXC by MAC address
def find_by_mac(mac_address):
    # Directories for VM and LXC configurations
    config_dirs = {
        "VM": "/etc/pve/qemu-server/",
        "LXC": "/etc/pve/lxc/"
    }

    for config_type, config_dir in config_dirs.items():
        # List all configuration files in each directory
        for config_file in os.listdir(config_dir):
            if config_file.endswith(".conf"):
                vmid = config_file.split(".")[0]  # Extract VMID from filename
                config_path = os.path.join(config_dir, config_file)

                # Open and search the config file for the MAC address
                with open(config_path, 'r') as file:
                    config_content = file.read()

                    # Use regex to find the MAC address in the file
                    if re.search(mac_address.lower(), config_content.lower()):
                        # Extract the VM or LXC name
                        name_match = re.search(r'name:\s*(\S+)', config_content)
                        name = name_match.group(1) if name_match else f"{config_type} {vmid}"

                        return vmid, name, config_type

    return None, None, None

# Function to start the VM or LXC
def start_instance(vmid, instance_type):
    try:
        # Use "qm" for VMs and "pct" for LXC containers
        if instance_type == "VM":
            subprocess.run(["qm", "start", vmid], check=True)
        elif instance_type == "LXC":
            subprocess.run(["pct", "start", vmid], check=True)

        # Get current date and time in a pretty format
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        print(f"{instance_type} {vmid} started at {current_time}.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to start {instance_type} {vmid}: {e}")

# Function to listen for magic packets (Wake-on-LAN)
def listen_for_wol():
    # Create a socket to listen for UDP packets on port 9 (standard WoL port)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.bind(("", 9))

    print("Listening for Wake-on-LAN packets...")

    while True:
        data, addr = s.recvfrom(1024)  # Receive UDP packet

        # Check for valid magic packet length (102 bytes for WoL packet)
        if len(data) >= 102:
            # Extract the MAC address from the packet
            mac = data[6:12].hex(':').upper()

            print(f"Received WoL packet for MAC: {mac}")

            # Dynamically find VM/LXC by MAC address
            vmid, name, instance_type = find_by_mac(mac)

            if vmid:
                print(f"Found {instance_type} {vmid} ({name}) for MAC {mac}. Starting...")
                start_instance(vmid, instance_type)
            else:
                print(f"No VM or LXC found with MAC {mac}.")

if __name__ == "__main__":
    listen_for_wol()
