from worker import Crawler
import pymysql
import re

baseUrl = "http://www.scjc.gov.cn"
indexUrl = "http://www.scjc.gov.cn/zhyw/qwfb/"


class SCCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        a = soup.find("div", class_="fenye txtc")
        ps = a.find_all("a")
        ll = len(ps)
        return int(ps[ll-3].text)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/zhyw/qwfb/index_"+str(i) + ".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("ul", class_="imglist_ul txtlist_ul hover_ul")
        tags = lists.find_all("a")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.get("href")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("h3", class_="article")
        info_result.title = title.text
        time_source = soup.find("p", class_="laiyuan").find_all("span")
        info_result.time = time_source[0].text
        info_result.source = time_source[1].text
        article = soup.find("div", class_="content_txt")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "四川"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布日期：", "")
        info.postion = "审查调查"
        return info

c = SCCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.scjc.gov.cn/zhyw/qwfb/index.html"))
# c.get_info("http://www.scjc.gov.cn/zhyw/qwfb/201806/106628829.html")
