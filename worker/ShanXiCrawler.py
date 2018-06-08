from worker import Crawler
import pymysql
import urllib.request
from bs4 import NavigableString
import re

baseUrl = "http://www.sxdi.gov.cn/"
indexUrl = baseUrl + "gzdt/jlsc/"
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/66.0.3359.117 Safari/537.36')]


class SXCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl, opener)
        num = soup.find("strong").text
        return int(num)+1

    def get_index(self):
        return None

    def join_url(self, i):
        url = baseUrl+"gzdt/jlsc/list_15_"+str(i)+".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url, opener)
        lists = soup.find("div", class_="mainleft fl")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.get('href')[1:]
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        while True:
            soup = self.get_soup(url, opener)
            if soup.find("meta").get("content") == "text/html; charset=gb2312":
                js = soup.find("script").text
                fa = re.findall('self.location=".*?"', js)[0]
                url = indexUrl + fa[16:-1]
            else:
                break
        title = soup.find("h1", class_="fl")
        info_result.title = title.text
        time_source = soup.find("span", class_="fl")
        ts = time_source.text.split("   ")
        info_result.time = ts[0]
        info_result.source = ts[1]
        article = soup.find("dd")
        ats = article.find_all("p")
        text = ""
        if len(ats) == 0:
            texts = article.contents
            for tx in texts:
                if isinstance(tx, NavigableString):
                    text = text + tx
            info_result.description = tx
        else:
            for at in ats:
                text = text + at.text.replace("\t", "").replace("\r", "")
            self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "山西"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "审查调查"
        return info

c = SXCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.join_url())
# print(c.get_urls("http://www.sdjj.gov.cn/tbbg/index_1.htm"))
# c.get_info("http://www.sxdi.gov.cn/gzdt/jlsc/2015020383.html")
