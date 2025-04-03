# PVE-WOL
ProxmoxVE python script that let's you use WakeOnLan (magic packets) to turn on VMs/LXCs

# Proxmox WoL Listener

A Python script that listens for **Wake-on-LAN (WoL)** packets and automatically starts the corresponding **VM or LXC container** process on a **PVE** host by matching the MAC address in its configuration file.

## Flow

- Listens for UDP WoL packets on port `9` (legacy)
- Parses MAC addresses from the magic packet
- Matches MAC against VM and LXC config files in:
  - `/etc/pve/qemu-server/` (Proxmox VMs)
  - `/etc/pve/lxc/` (Proxmox Containers)
- Starts the appropriate instance using `qm` or `pct`
- Logs startup timestamp and details to the console

## BONUS

In a Proxmox Cluster the /etc/pve filesysten is shared across them by default. As a result this will allow you to start VMs/LXCs across all your nodes with a single listener!
*This behaviour is confirmed with the listener running on the Master node. Behaviour might be node-specific if the listener is on a slave node. Test it and report back :)

## Requirements

- Proxmox VE host (tested on PVE 8)
- Python 3.6+
- Script must be run with permissions that allow reading `/etc/pve/` and running `qm`/`pct`

## Usage

1. Place the script on your Proxmox host (e.g., `/usr/local/bin/proxmox-wol-listener.py`).
2. Make it executable:
   ```bash
   chmod +x proxmox-wol-listener.py

## Demo