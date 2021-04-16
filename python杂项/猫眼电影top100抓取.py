'''猫眼电影top100抓取.py'''
import urllib.request
import re
import csv

class MaoyanSpider:
    def __init__(self):
        self.baseurl = "http://maoyan.com/board/4?offset="
        self.headers = {"User-Agent":"Mozilla/5.0"}
        self.page = 1
        self.offset = 0
        
    # 下载页面
    def loadPage(self,url):
        req = urllib.request.Request(url,headers=self.headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode("utf-8")
        self.parsePage(html)
        
    # 解析页面
    def parsePage(self,html):
        p = re.compile('<div class="movie-item-info">.*?title="(.*?)".*?<p class="star">(.*?)</p>.*?releasetime">(.*?)</p>',re.S)
        r_list = p.findall(html)
#        print(r_list)
        # [("霸王别姬","张国荣","1994-01-01"),(),()...]
        self.writePage(r_list)
    
    def writePage(self,r_list):
        if self.page == 1:
            with open("猫眼电影.csv","a",newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["电影名称","主演","上映时间"])
        for r_tuple in r_list:
            with open("猫眼电影.csv","a",newline="") as f:
                # 创建写入对象
                writer = csv.writer(f)
#                L = list(r_tuple)
                L = [r_tuple[0].strip(),r_tuple[1].strip(),r_tuple[2].strip()]
                # ["霸王别姬","张国荣","1994-01-01"]
                writer.writerow(L)
    
    def workOn(self):
        while True:
            c = input("爬取请按y(y/n):")
            if c.strip().lower() == "y":
                self.offset = (self.page-1)*10
                url = self.baseurl + str(self.offset)
                self.loadPage(url)
                self.page += 1
            else:
                print("爬取结束,谢谢使用!")
                break
                
if __name__ == "__main__":
    spider = MaoyanSpider()
    spider.workOn()     
        
        
        
        
        
        
        
        
        