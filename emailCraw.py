import sys
import getopt
import requests
from bs4 import BeautifulSoup
import re

def start(argv):
    url=""
    pages=""
    if len(sys.argv)<2:
        print('-h 帮助信息;/n')
        sys.exit()
    try:
        banner()
        opts,args=getopt.getopt(argv,"-u:-p:-h")
    except getopt.GetoptError:
        print("Error an argument")
        sys.exit()
    for opt,arg in opts:
        if opt=="-u":
            url=arg
        elif opt=="-p":
            pages=arg
        elif opt=="-h":
            print(usage())
    launcher(url,pages)

def banner():
    print('#######################################WELCOME MY FRIEND#####################################\n')

def usage():
    print('-h:--help 帮助;')
    print('-u:--url 域名;')
    print('-p:--pages 页数;')
    print('eg:python -u "www.baidu.com" -p 100'+'\n')
    sys.exit()

def launcher(url,pages):
    email_num=[]
    key_words=['email','mail','mailbox','邮件','邮箱','postbox']
    for page in range(1,int(pages)+1):
        for key_word in key_words:
            bing_emails=bing_search(url,page,key_word)
            baidu_emails=baidu_search(url,page,key_word)
            sum_emails=bing_emails+baidu_emails
            for email in sum_emails:
                if email in email_num:
                    pass
                else:
                    print(email)
                    with open('data.txt','a+') as f:
                        f.write(email+'\n')
                    email_num.append(email)

def bing_search(url,page,key_word):
    referer="http://cn.bing.com"
    conn=requests.session()
    bing_url="http://cn.bing.com/search?q="+key_word+"site%3a"+url+"&qs=n&sp=-1&pq="+key_word+"site%3a"+url+"&first="+str((page-1)*10)+"&FROM=PERE1"
    conn.get('http://cn.bing.com',headers=headers(referer))
    r=conn.get(bing_url,stream=True,headers=headers(referer),timeout=8)
    emails=search_email(r.text)
    return emails

def baidu_search(url,page,key_word):
    email_list=[]
    emails=[]
    referer="https://www.baidu.com"
    baidu_url="https://www.baidu.com/s?wd="+key_word+"site%3A"+url+"&pn="+str((page-1)*10)
    conn=requests.session()
    conn.get(referer,headers=headers(referer))
    r=conn.get(baidu_url,headers=headers(referer))
    soup=BeautifulSoup(r.text,'lxml')
    tagh3=soup.find_all('h3')
    for h3 in tagh3:
        href=h3.find('a').get('href')
        try:
            r=requests.get(href,headers=headers(referer),timeout=8)
            emails=search_email(r.text)
        except Exception as e:
            pass
        for email in emails:
            email_list.append(email)
    return email_list

def search_email(html):
    emails=re.findall(r"[a-z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+",html,re.I)
    return emails
def headers(referer):
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
             'Accept': '*/*',
             'Accept-Language': 'en-US,en;q=0.5',
             'Accept-Encoding': 'gzip,deflate',
             'Referer': referer
             }
    return headers

if __name__ == '__main__':
    try:
        start(sys.argv[1:])
    except KeyboardInterrupt:
        print('interrupted by user,killing all threads...')
