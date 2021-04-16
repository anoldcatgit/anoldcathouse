'''京东商品爬取.py'''
from selenium import webdriver
import time
import csv

# 接受用户输入,访问京东
pro = input("请输入要爬取的商品：")
driver = webdriver.Chrome()
driver.get("https://www.jd.com/")
i = 1
# 发送文字到搜索框,点击搜索
text = driver.find_element_by_class_name("text")
text.send_keys(pro)

button = driver.find_element_by_class_name("button")
button.click()
time.sleep(1)

while True:
    # 动态加载-->全部加载
    # 执行脚本,进度条拉到底部
    driver.execute_script(
       'window.scrollTo(0,\
        document.body.scrollHeight)')
    time.sleep(2) 
    # 正常解析爬取
    r_list = driver.find_elements_by_xpath\
          ('//div[@id="J_goodsList"]//li')

    # r为每一个商品的节点对象
    for r in r_list:
        m = r.text.split('\n')
        # ["￥52.80","Python...","200+",]
        price = m[0]
        name = m[1]
        commit = m[2]
        market = m[3]
        
        with open("商品.csv","a",newline="",encoding="gb18030") as f:
            writer = csv.writer(f)
            L = [name.strip(),price.strip(),
                 commit.strip(),market.strip()]
            writer.writerow(L)
    
    print("第%d页爬取成功" % i)
    i += 1
    # 点击下一页













