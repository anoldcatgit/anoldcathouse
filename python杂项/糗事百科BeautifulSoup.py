'''糗事百科BeautifulSoup.py'''
import requests
from bs4 import BeautifulSoup

url = "https://www.qiushibaike.com/"
headers = {"User-Agent":"Mozilla/5.0"}

res = requests.get(url,headers=headers)
res.encoding = "utf-8"
html = res.text

# 创建解析对象
soup = BeautifulSoup(html,'lxml')
r_list = soup.find_all("div",attrs={"class":"content"})

for r in r_list:
    s = r.span.get_text().strip()
    print(s)
    print("*" * 30)

















