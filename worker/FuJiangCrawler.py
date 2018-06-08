from worker import Crawler
import pymysql
import re

baseUrl = "http://www.fjcdi.gov.cn"
indexUrl = "http://www.fjcdi.gov.cn/html/xxgkajcc/"


class FJCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        a = soup.find("div", class_="list_foot")
        total = re.findall("1/[0-9]*页", a.text)[0]
        num = total[2:-1]
        return int(num)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/xxgkajcc/index_"+str(i+1) + ".jhtml"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", class_="news_list")
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
        title = soup.find("h2")
        info_result.title = title.text
        time_source = soup.find("div", class_="summary").text
        info_result.time = re.findall("浏览次数：.*?\n", time_source)[0].replace("浏览次数：","")
        info_result.source = re.findall("来源：.*? ", time_source)[0]
        article = soup.find("div", id="Info_Content")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "福建"
        info.source = info.source.replace("来源：", "")
        info.postion = "审查调查"
        return info

c = FJCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.fjcdi.gov.cn/xxgkajcc/index_2.jhtml"))
# c.get_info("http://www.fjcdi.gov.cn/html/xxgkajcc/20150515/1661900.html")
