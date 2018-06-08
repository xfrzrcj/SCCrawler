from worker import Crawler
import pymysql
import urllib.request
import re

baseUrl = "http://www.xzjjw.gov.cn"
indexUrl = "http://www.xzjjw.gov.cn/gz.php?type=97"
opener = urllib.request.build_opener()
opener.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                    'Chrome/66.0.3359.117 Safari/537.36')]


class XZCrawler(Crawler.CrawlerInterface):

    def get_num(self):
        soup = self.get_soup(indexUrl, opener)
        a = soup.find("script", language="JavaScript").text
        num = re.findall("page.pageCount =\d+;", a)[0]
        return int(num[16:-1])

    def get_index(self):
        return None

    def join_url(self, i):
        url = baseUrl + "/gz.php?type=97&page="+str(i)
        return url

    def get_urls(self, url):
        soup = self.get_soup(url, opener)
        lists = soup.find("div", class_="new_title")
        tags = lists.find_all("li")
        urls = []
        for tag in tags:
            info_url = baseUrl + "/" + tag.find("a").get('href')
            urls.append(info_url)
        return urls

    def get_info(self, url):
        info_result = Crawler.Info()
        info_result.url = url
        soup = self.get_soup(url, opener)
        title = soup.find("div", class_="title1")
        info_result.title = title.text
        time_source = soup.find("div", class_="time").text
        ts = time_source.split("   ")
        info_result.time = ts[1]
        info_result.source = ts[0]
        article = soup.find("div", class_="wrap_new").find("div", class_="main")
        ps = article.find_all("p")
        text = ""
        for p in ps:
            text = text + p.text + "\n"
        self.get_resum_description_from_text(text, info_result)
        return info_result

    def process_info(self, info):
        info.province = "西藏"
        info.source = info.source.replace("来源：", "")
        info.time = info.time.replace("发布时间：", "")
        info.postion = "审查调查"
        return info


c = XZCrawler()
conns = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='123456', db='data', charset='utf8')
c.start(conns)
conns.close()
# print(c.get_num())
# print(c.get_urls("http://www.xzjjw.gov.cn/gz.php?type=97&page=2"))
# c.get_info("http://www.xzjjw.gov.cn/gz_detail.php?id=42050")

