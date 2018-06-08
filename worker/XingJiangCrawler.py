from worker import Crawler
import pymysql
import urllib.request
import re

baseUrl = "http://www.xjjw.gov.cn"
indexUrl = "http://www.xjjw.gov.cn/zhuzhan/jilvjc/"
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/66.0.3359.117 Safari/537.36')]


class XJCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl, opener)
        a = soup.find_all("option")
        return len(a)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl + "/zhuzhan/jilvjc/index_"+str(i+1)+".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url, opener)
        lists = soup.find("ul", class_="cclist")
        tags = lists.find_all("li")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.find("a").get('href')
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url, opener)
        title = soup.find("h1", class_="ctitle")
        info_result.title = title.text
        time_source = soup.find("div", class_="msgbar").text
        ts = time_source.split("   ")
        info_result.time = ts[0]
        info_result.source = ts[1]
        article = soup.find("div", class_="newsCon")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "新疆"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "纪律审查"
        return info


c = XJCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.xjjw.gov.cn/zhuzhan/jilvjc/index_2.html"))
# c.get_info("http://www.xjjw.gov.cn/zhuzhan/jilvjc/20170601/13347.html")

