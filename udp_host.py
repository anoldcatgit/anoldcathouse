import time
from optparse import OptionParser
from random import randint
from scapy.all import *


def Scan(ip):
    try:
        dport = random.randint(1, 65535)
        packet = IP(dst=ip)/UDP(dport=dport)
        response = sr1(packet,timeout=1.0, verbose=0)
        if response:
            if int(response[IP].proto) == 1:
                time.sleep(0.5)
                print(ip + ' ' + "is up")
            else:
                print(ip + ' ' + "is down")
        else:
            print(ip + ' ' + "is down")
    except:
        pass


def main():
    usage = "Usage: %prog -i <ip address>"	# 输出帮助信息
    parse = OptionParser(usage=usage)
    parse.add_option("-i", '--ip', type="string", dest="targetIP", help="specify the IP address")	# 获取网段地址
    options, args = parse.parse_args()	#实例化用户输入的参数
    if '-' in options.targetIP:
        for i in range(int(options.targetIP.split('-')[0].split('.')[3]), int(options.targetIP.split('-')[1]) + 1):#192.168.1.12-122
            Scan(options.targetIP.split('.')[0] + '.' + options.targetIP.split('.')[1] + '.' + options.targetIP.split('.')[2] + '.' + str(i))
    else:
        Scan(options.targetIP)


if __name__ == '__main__':
    main()