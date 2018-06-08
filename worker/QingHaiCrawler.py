from worker import Crawler
import pymysql
import re

baseUrl = "http://www.qhjc.gov.cn"
indexUrl = "http://www.qhjc.gov.cn/html/ajcc/index.html"


class QHCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl)
        a = soup.find("a", text="尾页").get("href")
        nums = a.replace(".html", "").replace("index_", "")
        return int(nums)

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl+"/html/ajcc/index_"+str(i+1)+".html"
        return url

    def get_urls(self, url):
        soup = self.get_soup(url)
        lists = soup.find("div", "list")
        tags = lists.find_all("li")
        urls = []
        for tag in tags:
            info_url = baseUrl + tag.find("a").get("href")
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url)
        title = soup.find("div", class_="xl_tit1 tblack1")
        info_result.title = title.text
        time_source = soup.find("div", class_="xl_tit2").text
        info_result.time = re.findall("发布时间： \d{4}-|/\d{1,2}-|/\d{1,2}", time_source)[0]
        info_result.source = re.findall("文章来源：.*", time_source)[0]
        article = soup.find("div", class_="xl_con1")
        ps = article.find_all("div")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "青海"
        info.source = info.source.replace("文章来源：", "")
        info.time = info.time.replace("发布时间:", "")
        info.postion = "审查调查"
        return info

c = QHCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.qhjc.gov.cn/html/ajcc/index_2.html"))
# c.get_info("http://www.qhjc.gov.cn/html/2016318/n245029894.html")
