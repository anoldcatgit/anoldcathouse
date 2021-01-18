#!/usr/bin/python3
# -*- coding: utf-8 -*-

import nmap
import optparse

'''需要安装python-nmap
并下载nmap安装包 https://nmap.org/dist/nmap-7.80-setup.exe
把安装路径导入环境变量


'''
def NmapScan(targetIP):
    nm = nmap.PortScanner()
    try:

        result = nm.scan(hosts=targetIP, arguments='-sn -PE')
        state = result['scan'][targetIP]['status']['state']
        print("[{}] is [{}]".format(targetIP, state))
    except Exception  as e:
        pass


if __name__ == '__main__':
    parser = optparse.OptionParser('usage: python %prog -i ip \n\n'
                                    'Example: python %prog -i 192.168.1.1[192.168.1.1-100]\n')
    parser.add_option('-i','--ip',dest='targetIP',default='192.168.1.1',type='string',help='target ip address')
    options,args = parser.parse_args()

    if '-' in options.targetIP:
        for i in range(int(options.targetIP.split('-')[0].split('.')[3]),int(options.targetIP.split('-')[1])+1):
            NmapScan(options.targetIP.split('.')[0] + '.' + options.targetIP.split('.')[1] + '.' + options.targetIP.split('.')[2] + '.' + str(i))
    else:
        NmapScan(options.targetIP)