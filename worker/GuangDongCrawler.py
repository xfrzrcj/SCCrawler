from worker import Crawler
import pymysql
from selenium import webdriver
import time


baseUrl = "http://www.gdjct.gd.gov.cn"
indexUrl = "http://www.gdjct.gd.gov.cn/ffkb/index.jhtml"
browser = webdriver.Chrome("d:/chromedriver.exe")


class GDCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        pages = soup.find("div", class_="fanye").find_all("a")
        ll = len(pages)
        return int(pages[ll-2].text)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/ffkb/index_"+str(i+1)+".jhtml"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("ul", "GsTL5")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            su = tag.get("href").replace(":80", "")
            if su.startswith("http"):
                pass
            else:
                su = baseUrl + su
            urls.append(su)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        browser.get(url)
        time.sleep(0.5)
        title = browser.find_element_by_id("ScDetailTitle")
        info_result.title = title.text
        time_source = browser.find_element_by_class_name("desc")
        ts = time_source.text.split("      ")
        info_result.time = ts[1]
        info_result.source = ts[0]
        article = browser.find_element_by_id("ScDetailContent")
        ps = article.find_elements_by_tag_name("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "广东"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("日期：", "")
        info.postion = "反腐快报"
        return info

c = GDCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.gdjct.gd.gov.cn/ffkb/index_2.jhtml"))
# c.get_info("http://www.gdjct.gd.gov.cn/ffkb/62444.jhtml")
browser.quit()
