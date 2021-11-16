from re import VERBOSE
import scapy.all as scapy
import argparse
import requests
import time

parser = argparse.ArgumentParser()
parser.add_argument("--ip", help="Victim IP-Address")
parser.add_argument("--mac_scan", help="Flag for MAC-Scan")

args = parser.parse_args()

ip_addr = args.ip
flag = args.mac_scan

if flag:
    print("You used MAC-Scanning flag! It may take longer to scan network")

def getMACAddresses(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    request = broadcast/arp_request
    answered = scapy.srp(request, timeout=1, verbose=False)[0]
    print("IP\t\t\t\tMAC ADDRESS\n")
    for packet in answered:
        if flag:
            time.sleep(2)
            request = requests.get("https://api.macvendors.com/" + packet[1].hwsrc)
            print(request.text)
            print(packet[1].psrc + "\t\t\t" + packet[1].hwsrc + "\n")
        else:
            print(packet[1].psrc + "\t\t\t" + packet[1].hwsrc + "\n")

getMACAddresses(ip_addr)
