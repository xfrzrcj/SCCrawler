from worker import Crawler
import pymysql
import re
from selenium import webdriver
import time

baseUrl = "http://www.nxjjjc.gov.cn"
indexUrl = "http://www.nxjjjc.gov.cn/jlsc/qn/index.html"
zzqjlscUrl = "http://www.nxjjjc.gov.cn/jlsc/qn/zzqjlsc/index.html"
sxqjlscUrl = "http://www.nxjjjc.gov.cn/jlsc/qn/sxqjlsc/index.html"
browser = webdriver.Chrome("d:/chromedriver.exe")


class NXqnCrawler(Crawler.CrawlerInterface):

    def get_num(self):

        browser.get(indexUrl)
        a = browser.find_element_by_class_name("page").text
        nums = re.findall("共\d+页", a)[0][1:-1]
        return int(nums)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/jlsc/qn/index_"+str(i)+".html"
        return url

    def get_urls(self, url):
        browser.get(url)
        lists = browser.find_element_by_class_name("news-list")
        tags = lists.find_elements_by_tag_name("li")
        urls = []
        for tag in tags:
            info_url = tag.find_element_by_tag_name("a").get_attribute("href")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        browser.get(url)
        time.sleep(0.5)
        title = browser.find_element_by_class_name("tit")
        info_result.title = title.text
        ts = browser.find_element_by_class_name("bon").find_elements_by_tag_name("span")
        info_result.time = ts[1].text
        info_result.source = ts[0].text
        text = browser.find_element_by_class_name("TRS_Editor").text
        # text = article.find_element_by_tag_name("div").
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "宁夏"
        info.source = info.source.replace("稿件来源：", "")
        info.time = info.time.replace("发布时间:", "")
        info.postion = "区内，执纪审查"
        return info


class NXzzqjlscCrawler(Crawler.CrawlerInterface):

    def get_num(self):

        browser.get(zzqjlscUrl)
        a = browser.find_element_by_class_name("page").text
        nums = re.findall("共\d+页", a)[0][1:-1]
        return int(nums)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/jlsc/qn/zzqjlsc/index_"+str(i)+".html"
        return url

    def get_urls(self, url):
        browser.get(url)
        lists = browser.find_element_by_class_name("news-list")
        tags = lists.find_elements_by_tag_name("li")
        urls = []
        for tag in tags:
            info_url = tag.find_element_by_tag_name("a").get_attribute("href")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        browser.get(url)
        time.sleep(0.5)
        title = browser.find_element_by_class_name("tit")
        info_result.title = title.text
        ts = browser.find_element_by_class_name("bon").find_elements_by_tag_name("span")
        info_result.time = ts[1].text
        info_result.source = ts[0].text
        text = browser.find_element_by_class_name("TRS_Editor").text
        # text = article.find_element_by_tag_name("div").
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "宁夏"
        info.source = info.source.replace("稿件来源：", "")
        info.time = info.time.replace("发布时间:", "")
        info.postion = "区内，执纪审查"
        return info


class NXsxqjlscCrawler(Crawler.CrawlerInterface):

    def get_num(self):

        browser.get(sxqjlscUrl)
        a = browser.find_element_by_class_name("page").text
        nums = re.findall("共\d+页", a)[0][1:-1]
        return int(nums)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/jlsc/qn/sxqjlsc/index_"+str(i)+".html"
        return url

    def get_urls(self, url):
        browser.get(url)
        lists = browser.find_element_by_class_name("news-list")
        tags = lists.find_elements_by_tag_name("li")
        urls = []
        for tag in tags:
            info_url = tag.find_element_by_tag_name("a").get_attribute("href")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        browser.get(url)
        time.sleep(0.5)
        title = browser.find_element_by_class_name("tit")
        info_result.title = title.text
        ts = browser.find_element_by_class_name("bon").find_elements_by_tag_name("span")
        info_result.time = ts[1].text
        info_result.source = ts[0].text
        text = browser.find_element_by_class_name("TRS_Editor").text
        # text = article.find_element_by_tag_name("div").
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "宁夏"
        info.source = info.source.replace("稿件来源：", "")
        info.time = info.time.replace("发布时间:", "")
        info.postion = "区内，执纪审查"
        return info

c = NXsxqjlscCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.nxjjjc.gov.cn/jlsc/qn/index_1.html"))
# c.get_info("http://www.nxjjjc.gov.cn/jlsc/qn/201709/t20170911_4339798.html")
browser.quit()
