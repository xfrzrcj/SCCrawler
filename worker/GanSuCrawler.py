from worker import Crawler
import pymysql
import re

baseUrl = "http://www.gsjw.gov.cn"
indexUrl = "http://www.gsjw.gov.cn/category/jlsc"


class GSCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        a = soup.find("div", class_="page", id="page").text
        nums = re.findall("\d+/\d+ 页", a)[0][2:-1]
        return int(nums)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/category/jlsc/p/"+str(i+1)+".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("ul", class_="list")
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
        title = soup.find("h1")
        info_result.title = title.text
        time_source = soup.find("div", class_="infoBox").text
        info_result.time = re.findall("发布时间：\d{4}-|/\d{2}-|/\d{2} \d{2}:\d{2}", time_source)[0]
        info_result.source = re.findall("来源：.*? ", time_source)[0]
        article = soup.find("div", id="content")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "甘肃"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间:", "")
        info.postion = "审查调查"
        return info

c = GSCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.gsjw.gov.cn/category/jlsc/p/3.html"))
# c.get_info("http://www.gsjw.gov.cn/contents/9176.html")
