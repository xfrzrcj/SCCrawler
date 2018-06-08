from worker import Crawler
import pymysql
import re
from selenium import webdriver
import time

baseUrl = "http://www.qfyf.net"
indexUrl = "http://www.qfyf.net/col/col17/index.html"
browser = webdriver.Chrome("d:/chromedriver.exe")


class JSCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        a = soup.find("div", class_="c-sec-r-list").find_all("script")[5]
        total = re.findall("totalRecord:[0-9]+", a.text)[1]
        num = total.replace("totalRecord:", "")
        pages = int(num)
        if pages % 20 != 0:
            pages = pages // 20 + 1
        else:
            pages = pages // 20
        return pages

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/col/col17/index.html?uid=12606&pageNum="+str(i+1)
        return url

    def get_urls(self, url):
        browser.get(url)
        time.sleep(1)
        lists = browser.find_element_by_class_name("simple_pgContainer")
        tags = lists.find_elements_by_class_name("bt_link")
        urls = []
        for tag in tags:
            urls.append(tag.get_attribute("href"))
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("h1")
        info_result.title = title.text
        time_source = soup.find("div", class_="c-conten-top")
        ts = time_source.find_all("i")
        info_result.time = ts[0].text
        info_result.source = ts[2].text
        article = soup.find("div", class_="c-conten-con", id="c-conten-con")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "江苏"
        info.source = info.source.replace("信息来源：", "")
        info.time = info.time.replace("发布日期：", "")
        info.postion = "审查调查"
        return info

c = JSCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
browser.quit()
# print(c.get_num())
# print(c.get_urls("http://www.qfyf.net/col/col17/index.html?uid=12606&pageNum=1"))
# c.get_info("http://www.qfyf.net/art/2018/5/25/art_17_123135.html")
