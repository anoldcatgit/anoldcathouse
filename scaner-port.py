#!/usr/bin/python3
# -*- coding: utf-8 -*-
import sys
import socket
import optparse
import threading
import queue

class PortScanner(threading.Thread):
    def __init__(self,portqueue,ip,timeout=3):
        threading.Thread.__init__(self)
        self._portqueue=portqueue
        self._ip=ip
        self._timeout=timeout
    def run(self):
        while True:
            if self._portqueue.empty():
                break
            port=self._portqueue.get(timeout=0.5)
            try:
                s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
                s.settimeout(self._timeout)
                result_code=s.connect_ex((self._ip,port))
                if result_code ==0:
                    sys.stdout.write("[%d] OPEN\n" % port)
                else:
                    sys.stdout.write("[%d] CLOSED\n" % port)

            except Exception as e:
                print(e)
            finally:
                s.close()

def StartScan(targetip,port,threadNum):
    portList=[]
    portNumb=port
    if '-' in portNumb:
        for i in range(int(portNumb.split('-')[0]),int(portNumb.split('-')[1])+1):
            portList.append(i)
    else:
        portList.append(int(portNumb))
    ip=targetip
    threads=[]
    threadNumber=threadNum
    portQueue=queue.Queue()
    for port in portList:
        portQueue.put(port)
    for t in range(threadNumber):
        threads.append(PortScanner(portQueue,ip,timeout=3))
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    parser=optparse.OptionParser('Example:python %prog -i 127.0.0.1 -p 80 \n   python %prog -i 127.0.0.1 -p 1-100')
    parser.add_option('-i','--ip',dest='targetIP',default='127.0.0.1',type='string',help='target IP')
    parser.add_option('-p','--port',dest='port',default='80',type='string',help='scann port')
    parser.add_option('-t','--thread',dest='threadNum',default=1,type='int',help='scann thread number')
    (options,args)=parser.parse_args()

    StartScan(options.targetIP,options.port,options.threadNum)


