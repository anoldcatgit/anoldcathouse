import urllib.request
import re

class NeihanSpider:
    def __init__(self):
        self.baseurl = "https://www.neihan8.com/njjzw/"
        self.headers = {"User-Agent":"Mozilla/5.0"}
        self.page = 1
        
    # 下载页面
    def loadPage(self,url):
        req = urllib.request.Request(url,headers=self.headers)
        res = urllib.request.urlopen(req)
        html = res.read().decode("utf-8")
        self.parsePage(html)
        
    # 解析页面
    def parsePage(self,html):
        p = re.compile('<div class="text-.*?title="(.*?)".*?<div class="desc">(.*?)</div>',re.S)
        r_list = p.findall(html)
        # [("什么动物...","海豹"),(),()...]
        self.writePage(r_list)
        
    # 保存页面
    def writePage(self,r_list):
        for r_tuple in r_list:
            for r_str in r_tuple:
                with open("急转弯.txt","a",encoding="gb18030") as f:
                    f.write(r_str.strip() + "\n")
            with open("急转弯.txt","a",encoding="gb18030") as f:
                f.write("\n")
        
    def workOn(self):
        self.loadPage(self.baseurl)
        while True:
            c = input("成功,是否继续(y/n):")
            if c.strip().lower() == "y":
                self.page += 1
                url = self.baseurl + "index_" +\
                      str(self.page) + ".html"
                self.loadPage(url)
            else:
                print("爬取结束,谢谢使用!")
                break
                
if __name__ == "__main__":
    spider = NeihanSpider()
    spider.workOn()
    

    







