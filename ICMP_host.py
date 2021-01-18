#!/usr/bin/python
#coding:utf-8
from scapy.all import *
from random import randint
from optparse import OptionParser


'''运行前先在命令行输入scapy启动此模块
然后ifaces.reload()一下，ifaces会显示正常网卡信息
改默认网卡编号
conf.iface=ifaces.dev_from_index(14)
'''


def main():
    parser=OptionParser("Usage:%prog -i <target host>")
    parser.add_option('-i',type='string',dest='IP',help='specify target host')
    options,args=parser.parse_args()
    print("scan report for"+options.IP+"\n")
    if '-' in options.IP:
        for i in range(int(options.IP.split('-')[0].split('.')[3]),int(options.IP.split('-')[1])+1):
            Scan(options.IP.split('.')[0]+'.'+options.IP.split('.')[1]+'.'+options.IP.split('.')[2]+'.'+str(i))
            time.sleep(0.2)
    else:
        Scan(options.IP)

    print("\nScan finished!...\n")


def Scan(ip):
    ip_id=randint(1,65535)
    icmp_id=randint(1,65535)
    icmp_seq=randint(1,65535)
    packet=IP(dst=ip,ttl=64,id=ip_id)/ICMP(id=icmp_id,seq=icmp_seq)/b'rootkit'
    result=sr1(packet,timeout=1,verbose=False)
    if result:
        for rcv in result:
            scan_ip=rcv[IP].src
            print(scan_ip+'----->''Host is up!')
    else:
        print(ip+'----->''Host is down!')

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("interrupted by user ,killing all threads...")

