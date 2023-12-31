#!/usr/bin/env python
import argparse
import scapy.all as scapy

def get_ip():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Enter IP ranges")
    options = parser.parse_args()
    if not options.target:
        parser.error("[.] Please Specify an target IP range, use --help for more info")
    return options


def scan(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_request_broadcast = broadcast/arp_request
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]
    clients_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        clients_list.append(client_dict)
    return clients_list

def print_result(result_list):
    print("IP\t\t\tMAC Address\n----------------------------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])

scan_result = get_ip()
result = scan(scan_result.target)
print_result(result)
