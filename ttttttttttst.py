import os
import webbrowser

# # # os.system('"C:/Program Files/Internet Explorer/iexplore.exe" https://www.youdict.com/w/condone')
# # webbrowser.open("https://www.youdict.com/w/condone")
# # os.system('taskkill /F /IM chrome.exe')
#
# import requests
# from lxml import html
# url='https://www.youdict.com/w/condone' #需要爬数据的网址
# page=requests.Session().get(url)
# tree=html.fromstring(page.text)
# result=tree.xpath('//td[@class="title"]//a/text()') #获取需要的数据
#


import requests ##导入requests
from bs4 import BeautifulSoup ##导入bs4中的BeautifulSoup
import os





head = {'User-Agent':"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"}##浏览器请求头（大部分网站没有这个请求头会报错、请务必加上哦）
all_url = 'https://www.youdict.com/w/chronic'  ##开始的URL地址
start_html = requests.get(all_url,  headers=head, verify=False)  ##使用requests中的get方法来获取all_url(就是：http://www.mzitu.com/all这个地址)的内容 headers为上面设置的请求头、请务必参考requests官方文档解释
start_html.encoding='utf-8'

p = requests.get('http://icanhazip.com', headers=head)
print(p.text)


Soup = BeautifulSoup(start_html.text, 'lxml') ##使用BeautifulSoup来解析我们获取到的网页（‘lxml’是指定的解析器 具体请参考官方文档哦）
Soup = Soup.find(attrs={"id": "youdict"})
Soup = Soup.find_all(attrs={"class": "container"})[-1]
Soup = Soup.find(attrs={"class": "row"})
Soup = Soup.find(attrs={"class": "col-sm-8"})

Soup1 = Soup.find(attrs={"style": "font-family:SimSun,serif;"})
if Soup1 is not None:
    txt= Soup1.get_text()
    print(txt)

Soup2 = Soup.find(attrs={"id": "yd-ciyuan"})
if Soup2 is not None:
    txt = Soup2.get_text()
    print(txt)

# Soup3 = Soup.find(attrs={"id": "yd-etym"})
# if Soup3 is not None:
#     txt = Soup3.get_text()
#     print(txt)

