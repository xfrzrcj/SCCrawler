from worker import Crawler
import pymysql
import urllib.request
import re

baseUrl = "http://www.shjcw.gov.cn"
indexUrl = "http://www.shjcw.gov.cn/2015jjw/n2233/index.html"
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/66.0.3359.117 Safari/537.36')]


class SHCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl, opener)
        a = soup.find("span", class_="pageCount").text
        num = re.findall("/\d+", a)[0]
        return int(num[1:])

    def get_index(self):
        return indexUrl

    def join_url(self, i):
        url = baseUrl + "/2015jjw/n2233/index"+str(i)+".html"
        return url

    def get_urls(self, url):
        print(url)
        soup = self.get_soup(url, opener)
        lists = soup.find("ul", class_="newsList")
        tags = lists.find_all("li")
        urls = []
        for tag in tags:
            tt = tag.find("a")
            if tt is None:
                continue
            info_url = baseUrl + tag.find("a").get('href')
            urls.append(info_url)
        return urls

    def get_info(self, url):
        # if url == "http://www.shjcw.gov.cn/2015jjw/n2233/u1ai72497.html":
        #     print(1)
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url, opener)
        title = soup.find("div", id="ivs_title")
        info_result.title = title.text
        info_result.time = soup.find("span", class_="date").text
        source = soup.find("p", class_="source")
        if source is not None:
            info_result.source = source.text
        article = soup.find("div", id="ivs_content")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "上海"
        info.source = info.source.replace("来源：", "").replace("时间", "")
        info.time = info.time.replace("发表时间：", "")
        info.postion = "审查调查"
        return info


c = SHCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.shjcw.gov.cn/2015jjw/n2233/index1.html"))
# c.get_info("http://www.shjcw.gov.cn/2015jjw/n2233/u1ai64798.html")

