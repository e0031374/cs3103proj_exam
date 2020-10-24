import multiprocessing
import os
#os.sys.path.append("/home/owo/Documents/CS3103/proj2/venv/bin/")
import sys
from scapy.all import sr1, IP, ICMP, ARP, TCP, sniff 
from scapy.utils import PcapWriter
#from scapy import sr1,IP,ICMP

pktdump = PcapWriter("banana.pcap", append=True, sync=True)

def arp_monitor_callback(pkt):
    if ARP in pkt and pkt[ARP].op in (1,2): #who-has or is-at
        pkt.show()
        pktdump.write(pkt)
        return pkt.sprintf("%ARP.hwsrc% %ARP.psrc%")

def tcp_monitor_callback(pkt):
    #pktdump.write(pkt)
    if TCP in pkt: # and pkt[TCP].op in (1,2): #who-has or is-at
        pktdump.write(pkt)
        pkt.show()
        return pkt.sprintf("%TCP.hwsrc% %TCP.psrc%")

#sniff(prn=arp_monitor_callback, filter="arp", store=0)
#sniff(prn=tcp_monitor_callback, filter="tcp", store=0)
sniff(prn=tcp_monitor_callback, filter="tcp", store=0, timeout=1)
#timeout is in seconds

def print_hello():
    print("hello")

#

def monitor_fn():
    sniff(prn=tcp_monitor_callback, filter="tcp", store=0, timeout=10)


#p=sr1(IP(dst=sys.argv[1])/ICMP())
#if p:
#    p.show()


if __name__ == '__main__':
    monitor = multiprocessing.Process(target=monitor_fn)
    monitor.start()
    hello = multiprocessing.Process(target=print_hello)
    hello.start()
    monitor.join()
    hello.join()
    print("############### All stop ###################")
