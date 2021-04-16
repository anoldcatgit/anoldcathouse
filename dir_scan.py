 #coding:utf-8
import sys
import time
import random
import requests
import threading
from optparse import OptionParser
from queue import Queue

class DirScan:
    def __init__(self, options):
        self.url = options.url
        self.file_name = options.file_name
        self.numbers = options.numbers
    '''
    自定义Threading类继承Thread
    '''
    class Threading(threading.Thread):
        def __init__(self, queue, total):
            threading.Thread.__init__(self)
            self.sub_queue = queue
            self.sub_total = total
        '''
        重写run方法
        '''
        def run(self):
            while not self.sub_queue.empty():
                url = self.sub_queue.get()
                threading.Thread(target=self.progress).start()
                try:
                    r = requests.get(url=url, headers=self.get_user_agent(), timeout=4)
                    time.sleep(3)
                    if r.status_code == 200:
                        sys.stdout.write('\r' + '[--------]%s\n' % url)
                        result = open('result.html', 'a+') #追加写+读
                        result.write('<a href="' + url + '"target="_blank">' + url + '</a>')
                        result.write('\r\n</br>')
                        result.close()
                except Exception:
                    pass

        def progress(self):
            per = 100 - float(self.sub_queue.qsize()) / float(self.sub_total) * 100
            percent = "%s Items Complete in %1.f %s" % (
                (self.sub_total - self.sub_queue.qsize()), per, '%')
            sys.stdout.write('\r' + '[*]' + percent)

        def get_user_agent(self):
            user_agent_list = [{
                                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'},
                               {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'},
                               {
                                   'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50'},
                               {
                                   'User-Agent': 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0; .NET CLR 2.0.50727; SLCC2; .NET CLR 3.5.30729; .NET CLR 3.0.30729; Media Center PC 6.0; InfoPath.3; .NET4.0C; Tablet PC 2.0; .NET4.0E)'}
                               ]
            return random.choice(user_agent_list)

    def startscan(self):
        result = open('result.html', 'w') # 以写方式打开
        result.close()
        queue = Queue()
        f = open('dict.txt', 'r')
        for i in f.readlines():
            queue.put(self.url + "/" + i.strip('\n'))
            total = queue.qsize()
        threads = []
        thread_count = int(self.numbers)
        for i in range(thread_count):
            threads.append(self.Threading(queue, total))
        for thread in threads:
            thread.start()
            thread.join()

def main():
    print("     ___   ___  __ _  _____          ")
    print("    / __| / __|/ _  ||  _  |     __  ")
    print("    \__ \| (__| (_| || | | |  | |  | ")
    print("    |___/ \___|\__,_||_| |_|  |.|__| ")
    print("Welcome to my NOOB DirScan ver1.0")
    parser = OptionParser('python dir_scan.py -u <Target URL> -f <Dictionary File Name> -t <Thread numbers>')
    parser.add_option('-u', '--url', dest='url', type='string', help='the URL you wanna scan(such as http://123.206.84.240:9000)')
    parser.add_option('-f', '--file', dest='file_name', type='string', help='the dictionary you wanna choose')
    parser.add_option('-t', '--thread', dest='numbers', type='int', help='the number of threads you wanna choose')
    (options, args) = parser.parse_args()
    if options.url and options.file_name:
        dirscan = DirScan(options)
        dirscan.startscan()
        sys.exit(1)
    else:
        parser.print_help()
        sys.exit(1)

if __name__=='__main__':
    main()
