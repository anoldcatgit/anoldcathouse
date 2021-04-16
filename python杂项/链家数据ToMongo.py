'''链家数据ToMongo.py'''
import requests
import re
import pymongo

class LianjiaSpider:
    def __init__(self):
        self.baseurl = "https://bj.lianjia.com/ershoufang/pg"
        self.page = 1
        self.headers = {"User-Agent":"Mozilla/5.0"}
        self.proxies = {"http":"http://309435365:szayclhp@123.206.119.108:16817"}
        self.conn = pymongo.MongoClient("localhost",27017)
        self.db = self.conn.Lianjia
        self.myset = self.db.housePrice

    def getPage(self,url):
        res = requests.get(url,proxies=self.proxies,headers=self.headers,timeout=5)
        res.encoding = "utf-8"
        html = res.text
        print("页面爬取成功,正在解析...")
        self.parsePage(html)

    def parsePage(self,html):
        p = re.compile('<div class="houseInfo".*?data-el="region">(.*?)</a>.*?<div class="totalPrice">.*?<span>(.*?)</span>(.*?)</div>',re.S)
        r_list = p.findall(html)
        # [("天通苑","480","万"),()..]
        print("页面解析完成,正在存入数据库...")
        self.writeTomongo(r_list)

    def writeTomongo(self,r_list):
        for r_tuple in r_list:
            D = {"houseName":r_tuple[0].strip(),\
            "totalPrice":float(r_tuple[1].strip())*10000}
            self.myset.insert(D)
        print("存入数据库成功")

    def workOn(self):
        while True:
            c = input("爬取按y(q退出):")
            if c.strip().lower() == "y":
                url = self.baseurl + str(self.page) + "/"
                self.getPage(url)
                self.page += 1
            else:
                print("爬取结束,谢谢使用!")
                break



if __name__ == "__main__":
    spider = LianjiaSpider()
    spider.workOn()
