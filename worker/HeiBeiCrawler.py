from worker import Crawler
import pymysql
from urllib.error import HTTPError

baseUrl = "http://www.hebcdi.gov.cn/"
indexUrl = baseUrl + "node_122866.htm"


class HeiBeiZjscCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        pas = soup.find_all("a", class_="page-Article")
        num = ""
        for pa in pas:
            num = pa.text
        return int(num)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl + "node_122866_" + str(i+1) + ".htm"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", class_="feed")
        tags = lists.find_all("div", class_="feed-item")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.find("a").get("href")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        try:
            soup = self.get_soup(url)
        except HTTPError as e:
            print("can't find " + url)
            print(e)
            return None
        info_result.url = url
        info_result.url = url
        title = soup.find("h1")
        info_result.title = title.text
        time_source = soup.find("div", class_="min_cc")
        ts = time_source.text.split("发布时间：")
        info_result.time = ts[1]
        info_result.source = ts[0]
        article = soup.find("div", class_="min_content")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "河北"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "执纪审查"
        return info


class HeiBeiDjzwcfCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup("http://www.hebcdi.gov.cn/node_124627.htm")
        pas = soup.find_all("a", class_="page-Article")
        num = ""
        for pa in pas:
            num = pa.text
        return int(num)

    def get_index(self):
        return "http://www.hebcdi.gov.cn/node_124627.htm"

    def join_url(self, i):
        url = baseUrl + "node_124627_" + str(i+1) + ".htm"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", class_="feed")
        tags = lists.find_all("div", class_="feed-item")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.find("a").get("href")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        try:
            soup = self.get_soup(url)
        except HTTPError as e:
            print("can't find " + url)
            print(e)
            return None
        info_result.url = url
        info_result.url = url
        title = soup.find("h1")
        info_result.title = title.text
        time_source = soup.find("div", class_="min_cc")
        ts = time_source.text.split("发布时间：")
        info_result.time = ts[1]
        info_result.source = ts[0]
        article = soup.find("div", class_="min_content")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "河北"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "党纪政务处分"
        return info


c = HeiBeiDjzwcfCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
#print(c.join_url(1))
# print(c.get_urls("http://www.hebcdi.gov.cn/node_122866_20.htm"))
# c.get_info("http://www.hebcdi.gov.cn/2018-04/26/content_6861030.htm")
